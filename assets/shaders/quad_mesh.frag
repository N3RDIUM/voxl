#version 330 core

in vec2 v_uv;
flat in float v_tex_index;
in float v_fog_distance;
flat in float v_orientation;

out vec4 out_color;

uniform sampler2DArray textures;
uniform vec3 fog_color = vec3(0.5, 0.69, 1.0);

// Simple per-face light factors
// Order: +Z (front), -Z (back), -X (left), +X (right), +Y (top), -Y (bottom)
const float face_light[6] = float[](
    0.8,   // FRONT
    0.7,   // BACK
    0.6,   // LEFT
    0.9,   // RIGHT
    1.0,   // TOP
    0.5    // BOTTOM
);

void main() {
    vec4 tex_color = texture(textures, vec3(v_uv, v_tex_index));

    // Apply flat face lighting
    float light = face_light[int(v_orientation)];
    tex_color.rgb *= light;

    // Fog calculation
    float fog_factor = exp(-v_fog_distance * 0.01);
    out_color = mix(vec4(fog_color, tex_color.a), tex_color, fog_factor);
}
