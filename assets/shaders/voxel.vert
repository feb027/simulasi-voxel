#version 330 core

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec2 a_uv;
layout (location = 2) in vec3 a_normal;
layout (location = 3) in float a_face_shade;

uniform mat4 u_projection;
uniform mat4 u_view;

out vec2 v_uv;
out vec3 v_normal;
out vec3 v_world_pos;
out float v_face_shade;

void main() {
    v_uv = a_uv;
    v_normal = a_normal;
    v_world_pos = a_position;
    v_face_shade = a_face_shade;
    gl_Position = u_projection * u_view * vec4(a_position, 1.0);
}
