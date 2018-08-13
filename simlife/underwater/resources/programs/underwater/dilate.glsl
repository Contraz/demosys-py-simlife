#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

smooth out vec2 uv;

void main(void) {
  uv = in_uv;
  gl_Position = vec4(in_position, 1.0);
}


#elif defined FRAGMENT_SHADER

out vec4 fragColor;

uniform sampler2D texture0;
uniform float viewportStep;

smooth in vec2 uv;

void main(void)
{
	vec4 sum;
	sum = texture(texture0, uv);

	// Top Left
	sum += texture(texture0, uv + vec2(-viewportStep, viewportStep));

	// Top Center
	sum += texture(texture0, uv + vec2(0.0, viewportStep));

	// Top Right
	sum += texture(texture0, uv + vec2(viewportStep, viewportStep));


	// Center Left
	sum += texture(texture0, uv + vec2(viewportStep, 0.0));

	// Center
	sum += texture(texture0, uv + vec2(0.0, 0.0));

	// Center Right
	sum += texture(texture0, uv + vec2(-viewportStep, 0.0));


	// Bottom Left
	sum += texture(texture0, uv + vec2(-viewportStep, -viewportStep));

	// Bottom Center
	sum += texture(texture0, uv + vec2(0.0, -viewportStep));

	// Bottom Right
	sum += texture(texture0, uv + vec2(viewportStep, -viewportStep));


	fragColor = vec4(sum.xyz, 1.0);
}

#endif