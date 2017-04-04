#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

smooth out vec2 uv;

void main(void)
{
	uv = in_uv;
	gl_Position = vec4(in_position, 1.0);
}


#elif defined FRAGMENT_SHADER

out vec4 fragColor;

uniform sampler2D texture0;
uniform float viewportStep;
uniform float contrast;
uniform vec3 color;

smooth in vec2 uv;

void main(void)
{
	vec4 sum;
	sum = texture(texture0, uv) * -4.0;

	// Top
	sum += texture(texture0, uv + vec2(0.0, viewportStep)) * 1.0;
	// Bottom
	sum += texture(texture0, uv + vec2(0.0, -viewportStep)) * 1.0;
	// Left
	sum += texture(texture0, uv + vec2(viewportStep, 0.0)) * 1.0;
	// Right
	sum += texture(texture0, uv + vec2(-viewportStep, 0.0)) * 1.0;

	fragColor = vec4(sum.xyz * color.xyz, 1.0) * contrast;
}



#endif