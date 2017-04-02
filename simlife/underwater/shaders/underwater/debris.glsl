#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_color;
uniform mat4 m_mv;
out vec3 vs_color;

void main() {
    float dist = -(m_mv * vec4(in_position, 1.0)).z;
    if(dist < 2.0) {
        vs_color = in_color * (dist - 1.0);
    }
    else {
        vs_color = in_color;
    }

    gl_Position = vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;
in vec2 geo_uv;
in vec3 geo_color;

void main() {
    fragColor = texture(texture0, geo_uv) * vec4(geo_color, 1.0);
}

#elif defined GEOMETRY_SHADER

layout(points) in;
layout(triangle_strip, max_vertices = 4) out;

uniform mat4 m_proj;
uniform mat4 m_mv;
uniform float size;

in vec3 vs_color[];

out vec2 geo_uv;
out vec3 geo_color;

#define EMIT_V(POS, UV) \
	gl_Position = m_proj * m_mv * vec4(POS, 1.0); \
	geo_uv = UV; \
	geo_color = vs_color[0]; \
	EmitVertex();

void main() {
    // Billboard
    vec3 right = vec3(m_mv[0][0], m_mv[1][0], m_mv[2][0]);
    vec3 up = vec3(m_mv[0][1], m_mv[1][1], m_mv[2][1]);

    EMIT_V(gl_in[0].gl_Position.xyz - (right + up) * size, vec2(1.0, 1.0));
    EMIT_V(gl_in[0].gl_Position.xyz - (right - up) * size, vec2(0.0, 1.0));
    EMIT_V(gl_in[0].gl_Position.xyz + (right - up) * size, vec2(1.0, 0.0));
    EMIT_V(gl_in[0].gl_Position.xyz + (right + up) * size, vec2(0.0, 0.0));
    EndPrimitive();
}

#endif
