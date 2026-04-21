#version 330 core

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;
layout (location = 2) in vec3 a_normal;

uniform mat4 u_projection;
uniform mat4 u_view;

out vec3 v_color;
out vec3 v_normal;
out vec3 v_world_pos;

void main() {
    v_color = a_color;
    v_normal = a_normal;
    v_world_pos = a_position;
    gl_Position = u_projection * u_view * vec4(a_position, 1.0);
}

