#version 330

//#include Includes.txt

vec4 screen(vec4 color0, vec4 color1) {
    vec4 white = vec4(1.0, 1.0, 1.0, 1.0);
    return white - ((white - color0) * (white - color1));
}

uniform sampler2D source0;
uniform sampler2D source1;

out vec4 fragColor;
in vec2 out_uv;

void main() {
	fragColor = screen(texture2D(source0, out_uv), texture2D(source1, out_uv));
}
