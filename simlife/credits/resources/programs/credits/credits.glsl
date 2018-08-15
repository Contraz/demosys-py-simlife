#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

out vec2 uv;

void main() {
	gl_Position = vec4(in_position, 1.0);
    uv = in_uv;
}

#elif defined FRAGMENT_SHADER
//#include Includes.txt

vec4 screen(vec4 color0, vec4 color1) {
    vec4 white = vec4(1.0, 1.0, 1.0, 1.0);
    return white - ((white - color0) * (white - color1));
}

out vec4 fragColor;

uniform sampler2D source0;
uniform sampler2D source1;
uniform float source0_opacity;
uniform float source1_opacity;
uniform vec2 position;
uniform vec2 scale;

in vec2 uv;

void main() 
{
	vec2 texcoord = vec2(0.5, 0.5) + (uv + vec2(-0.5, -0.5) * scale) + position;
	fragColor = screen(
        texture2D(source0, texcoord) * vec4(source0_opacity),
        texture2D(source1, uv) * vec4(source1_opacity)
    );
}
#endif
