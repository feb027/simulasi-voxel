#version 330 core

in vec2 v_uv;
in vec3 v_normal;
in vec3 v_world_pos;
in float v_face_shade;

uniform vec3 u_camera_pos;
uniform vec3 u_fog_color;
uniform vec3 u_sun_direction;
uniform vec3 u_light_color;
uniform float u_ambient_strength;
uniform float u_diffuse_strength;
uniform sampler2D u_texture_atlas;

out vec4 frag_color;

void main() {
    vec3 albedo = texture(u_texture_atlas, v_uv).rgb;
    vec3 normal = normalize(v_normal);
    vec3 light_dir = normalize(u_sun_direction);
    float diffuse = max(dot(normal, light_dir), 0.0);
    float lighting = u_ambient_strength + diffuse * u_diffuse_strength;
    vec3 lit = albedo * lighting * u_light_color * v_face_shade;

    float distance_to_camera = distance(v_world_pos, u_camera_pos);
    float fog_factor = clamp((distance_to_camera - 18.0) / 70.0, 0.0, 1.0);
    vec3 final_color = mix(lit, u_fog_color, fog_factor);
    frag_color = vec4(final_color, 1.0);
}
