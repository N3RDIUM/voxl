import unittest

import numpy as np
from voxl.core.compute import ComputeManager, ComputePipeline


class TestCompute(unittest.TestCase):
    def test_double(self):
        manager = ComputeManager({
            "power_preference": "high-performance"
        })

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
