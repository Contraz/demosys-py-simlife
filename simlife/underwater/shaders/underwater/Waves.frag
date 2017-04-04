uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform sampler2D tex3;

uniform float scroll0;
uniform float scroll1;
uniform float scroll2;

varying vec4 diffuse;
varying vec4 ambientGlobal;
varying vec4 ambient;
varying vec3 normal;
varying float dist;
varying vec3 lightDir;
varying vec3 halfVector;

void main() {
	vec3 n;
	vec3 halfV;
	vec3 viewV;
	float NdotL;
	float NdotHV;
	vec4 color = ambientGlobal;
	float att;

	n = normalize(normal);

	NdotL = max(dot(n,normalize(lightDir)),0.0);
	if (NdotL > 0.0) {

		att = 1.0 / (gl_LightSource[0].constantAttenuation +
				gl_LightSource[0].linearAttenuation * dist +
				gl_LightSource[0].quadraticAttenuation * dist * dist);
		color += att * (diffuse * NdotL + ambient);
		halfV = normalize(halfVector);

		NdotHV = max(dot(n,halfV),0.0);
		color += att * gl_FrontMaterial.specular * gl_LightSource[0].specular *
						pow(NdotHV,gl_FrontMaterial.shininess);
	}

	float step = 1.0 / 2048.0;
	vec2 txc = gl_TexCoord[0].xy * 3.75;

	vec2 norms0 = texture2D(tex0, txc + vec2(scroll0, 0.0)).rg;
	vec2 norms1 = texture2D(tex1, txc + vec2(0.0,  scroll1)).rg;
	vec2 norms2 = texture2D(tex2, txc + vec2(scroll2, scroll2)).rg;
	
	vec2 final_norms = (norms0 * norms1 * norms2);

	gl_FragColor = color * (texture2D(tex3, gl_TexCoord[0].xy + final_norms) * 14.0);
}
