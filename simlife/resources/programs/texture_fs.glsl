#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

smooth out vec2 uv;

void main() {
    uv = in_uv;
    gl_Position = vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;
smooth in vec2 uv;

void main() {
    fragColor = texture(texture0, uv);
}

#endif
