#version 410

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_mv;
uniform sampler2D floor_map;

out float color;

void main() {
    float dist = -(m_mv * vec4(in_position, 1.0)).z;
    color = 0.8 - dist / 100.0;

    float y_offset = texture(floor_map, in_position.xz / 200.0 - vec2(0.5, 0.5)).b * 20.0;
    y_offset = min(y_offset, 7.0) - 7.0;

    gl_Position = m_proj * m_mv * vec4(in_position + vec3(1.0, y_offset, 1.0), 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
in float color;

void main() {
    fragColor = vec4(1.0) * color;
}


#endif
