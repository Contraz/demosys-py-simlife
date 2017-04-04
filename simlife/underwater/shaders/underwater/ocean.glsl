#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

uniform mat4 m_proj;
uniform mat4 m_mv;
uniform mat3 m_normal;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;

uniform float scroll0;
uniform float scroll1;
uniform float scroll2;

out vec2 uv;
out vec3 normal;

out vec3 lightDir;
out vec3 halfVector;
out float dist;

void main() {
	vec3 aux;
	normal = normalize(m_normal * vec3(0.0, 1.0, 0.0));
	vec4 ecPos = m_mv * vec4(in_position, 1.0);
	aux = vec3(ecPos);
	lightDir = normalize(aux);
	dist = length(aux);

	halfVector = normalize(in_position); // ****

    uv = in_uv;

	vec2 txc = in_uv / 2.0;

	vec2 norms0 = texture(tex0, txc + vec2(scroll0 / 1.0, 0.0)).rg;
	vec2 norms1 = texture(tex1, txc + vec2(0.0,  scroll1 / 1.0)).rg;
	vec2 norms2 = texture(tex2, txc + vec2(scroll2, scroll2)).rg;

	vec2 final_norms = norms0 * norms1 * norms2;

	gl_Position = m_proj * m_mv * (vec4(0.0, final_norms.x * 16.0, 0.0, 0.0) + vec4(in_position, 1.0));
}


#elif defined FRAGMENT_SHADER

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform sampler2D tex3;

uniform float scroll0;
uniform float scroll1;
uniform float scroll2;

in vec2 uv;
in vec3 normal;
in vec3 lightDir;
in vec3 halfVector;
in float dist;

void main() {
	vec3 n;
	vec3 halfV;
	vec3 viewV;
	float NdotL;
	float NdotHV;
	vec4 color =  vec4(0.0, 0.0, 0.0, 1.0); //ambientGlobal;
	float att;

	n = normalize(normal);

	NdotL = max(dot(n, normalize(lightDir)), 0.0);
	if (NdotL > 0.0) {

//		att = 1.0 / 100.0 + 100.0 * dist + 100.0 * dist * dist);
        att = 0.5 - dist / 300.0;
//        att = 1.0;

		color += att * (vec4(1.0) * NdotL); // + ambient);
		halfV = normalize(halfVector);

		NdotHV = max(dot(n, halfV), 0.0);
//		color += att * gl_FrontMaterial.specular * gl_LightSource[0].specular *
//						pow(NdotHV,gl_FrontMaterial.shininess);
	}

	float step = 1.0 / 2048.0;
	vec2 txc = uv * 3.75;

	vec2 norms0 = texture(tex0, txc + vec2(scroll0, 0.0)).rg;
	vec2 norms1 = texture(tex1, txc + vec2(0.0,  scroll1)).rg;
	vec2 norms2 = texture(tex2, txc + vec2(scroll2, scroll2)).rg;

	vec2 final_norms = (norms0 * norms1 * norms2);

	fragColor = color * (texture(tex3, uv + final_norms) * 14.0);
}

#endif
