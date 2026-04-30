#version 330 core

in vec2 v_uv;
out vec4 frag_color;

uniform int u_crack_stage;   // 0–9

// --- simple hash helpers for procedural cracks ---
float hash21(vec2 p) {
    p = fract(p * vec2(123.34, 456.21));
    p += dot(p, p + 45.32);
    return fract(p.x * p.y);
}

float hash11(float p) {
    p = fract(p * 0.1031);
    p *= p + 33.33;
    p *= p + p;
    return fract(p);
}

// cell noise that returns distance-to-nearest-point  (Worley-ish)
float cellNoise(vec2 uv, float density) {
    vec2 id = floor(uv * density);
    vec2 gv = fract(uv * density);
    float minDist = 1.0;

    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            vec2 offset = vec2(float(x), float(y));
            vec2 n = vec2(hash21(id + offset), hash21((id + offset) * 1.7));
            vec2 diff = offset + n - gv;
            minDist = min(minDist, length(diff));
        }
    }
    return minDist;
}

void main() {
    if (u_crack_stage <= 0) {
        discard;
    }

    float stage = float(u_crack_stage);          // 1..9
    float intensity = stage / 9.0;               // 0.11 .. 1.0

    // Two layers of cracks at different scales
    float c1 = cellNoise(v_uv, 3.0 + stage);
    float c2 = cellNoise(v_uv * 1.5 + 0.37, 4.0 + stage * 0.7);

    // Edge/crack detection: lower values = closer to a cell edge
    float crack = min(c1, c2);

    // Threshold narrows (more cracks visible) as intensity grows
    float threshold = mix(0.08, 0.28, intensity);
    float alpha = smoothstep(threshold, 0.0, crack) * intensity;

    // Dark overlay colour
    vec3 color = vec3(0.0, 0.0, 0.0);
    frag_color = vec4(color, alpha * 0.85);
}
