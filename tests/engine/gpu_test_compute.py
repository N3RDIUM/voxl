import unittest
from typing import final

import numpy as np
from typing_extensions import override

from src.engine.compute import ComputeManager, ComputePipeline


@final
class TestCompute(unittest.TestCase):
    @classmethod
    @override
    def setUpClass(cls):
        cls.manager = ComputeManager({"power_preference": "high-performance"})

    def test_wgsl_double(self):
        manager = self.manager

        shader = """
        @group(0) @binding(0)
        var<storage, read_write> data: array<f32>;

        @compute @workgroup_size(64)
        fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
            let i = gid.x;
            if (i < arrayLength(&data)) {
                data[i] = data[i] * 2.0;
            }
        }
        """
        pipeline = ComputePipeline(shader, "main", manager)

        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float32)
        expected_result = data * 2

        buffer = manager.buffer_from_np(data)
        n = data.size

        manager.enqueue(
            pipeline,
            bindings={
                0: {  # group 0
                    0: buffer  # binding 0
                }
            },
            n_workgroups=((n + 63) // 64, 1, 1),
        )

        manager.compute_pass()

        result = manager.readback(buffer=buffer, nbytes=data.nbytes, dtype="f")

        self.assertEqual(list(result), list(expected_result))

    def test_multiple_dispatches(self):
        manager = self.manager

        shader = """
        @group(0) @binding(0)
        var<storage, read_write> data: array<f32>;

        @compute @workgroup_size(64)
        fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
            let i = gid.x;
            if (i < arrayLength(&data)) {
                data[i] = data[i] * 2.0;
            }
        }
        """
        pipeline = ComputePipeline(shader, "main", manager)

        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float32)
        expected_result = data * 2 * 2

        buffer = manager.buffer_from_np(data)
        n = data.size

        manager.enqueue(
            pipeline,
            bindings={0: {0: buffer}},
            n_workgroups=((n + 63) // 64, 1, 1),
        )

        manager.enqueue(
            pipeline,
            bindings={0: {0: buffer}},
            n_workgroups=((n + 63) // 64, 1, 1),
        )

        manager.compute_pass()

        result = manager.readback(buffer=buffer, nbytes=data.nbytes, dtype="f")

        self.assertEqual(list(result), list(expected_result))

    def test_multiple_bind_groups(self):
        manager = self.manager

        shader = """
        @group(0) @binding(0)
        var<storage, read> a: array<f32>;

        @group(0) @binding(1)
        var<storage, read> b: array<f32>;

        @group(0) @binding(2)
        var<storage, read_write> output: array<f32>;

        @compute @workgroup_size(64)
        fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
            let i = gid.x;
            if (i < arrayLength(&output)) {
                output[i] = a[i] + b[i];
            }
        }
        """
        pipeline = ComputePipeline(shader, "main", manager)

        a = np.array([1.0, 2.0, 3.0], dtype=np.float32)
        b = np.array([10.0, 20.0, 30.0], dtype=np.float32)
        expected_result = a + b

        buffer_a = manager.buffer_from_np(a)
        buffer_b = manager.buffer_from_np(b)
        buffer_output = manager.buffer_from_np(np.zeros_like(a))

        n = a.size

        manager.enqueue(
            pipeline,
            bindings={
                0: {
                    0: buffer_a,
                    1: buffer_b,
                    2: buffer_output,
                }
            },
            n_workgroups=((n + 63) // 64, 1, 1),
        )

        manager.compute_pass()

        result = manager.readback(
            buffer=buffer_output, nbytes=a.nbytes, dtype="f"
        )

        self.assertEqual(list(result), list(expected_result))
