#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

uniform mat4 m_proj;
uniform mat4 m_mv;

void main() {
	vec3 aux;
	aux = vec3(ecPos);
	lightDir = normalize(aux);
	dist = length(aux);
	halfVector = normalize(vec3(0.5)); // ****



}


#elif defined FRAGMENT_SHADER

out vec4 fragColor;


void main() {



}

