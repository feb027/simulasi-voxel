#version 330 core

in vec2 v_uv;

uniform vec3 u_color;
uniform float u_visibility;
uniform float u_core_strength;
uniform float u_halo_strength;
uniform float u_halo_radius;
uniform float u_edge_softness;

out vec4 frag_color;

void main() {
    vec2 p = v_uv * 2.0 - vec2(1.0);
    float r = length(p);
    if (r > u_halo_radius) {
        discard;
    }

    float core = smoothstep(0.65, 0.0, r);
    float halo = smoothstep(u_halo_radius, 0.0, r);
    float corona_band = smoothstep(0.95, 0.45, r) * (1.0 - smoothstep(0.45, 0.18, r));
    // Fade out near the quad's diagonal limit to avoid visible square edges.
    float quad_fade = 1.0 - smoothstep(1.26, 1.41421356, r);

    float emissive = core * u_core_strength + halo * u_halo_strength + corona_band * u_halo_strength * 0.35;
    float alpha = clamp((core + halo * u_edge_softness) * u_visibility * quad_fade, 0.0, 1.0);
    vec3 color = u_color * emissive * u_visibility * quad_fade;

    frag_color = vec4(color, alpha);
}
