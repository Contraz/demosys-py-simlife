uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;

uniform float scroll0;
uniform float scroll1;
uniform float scroll2;

varying vec4 diffuse;
varying vec4 ambientGlobal;
varying vec4 ambient;
varying vec3 normal;
varying vec3 lightDir;
varying vec3 halfVector;
varying float dist;


void main() {
	vec4 ecPos;
	vec3 aux;
	normal = normalize(gl_NormalMatrix * gl_Normal);

	ecPos = gl_ModelViewMatrix * gl_Vertex;
	aux = vec3(gl_LightSource[0].position-ecPos);
	lightDir = normalize(aux);
	dist = length(aux);
	halfVector = normalize(gl_LightSource[0].halfVector.xyz);

	diffuse = gl_FrontMaterial.diffuse * gl_LightSource[0].diffuse;
	ambient = gl_FrontMaterial.ambient * gl_LightSource[0].ambient;
	ambientGlobal = gl_LightModel.ambient * gl_FrontMaterial.ambient;
    
    
	gl_TexCoord[0] = gl_MultiTexCoord0;

	vec2 txc = gl_TexCoord[0].xy / 2.0;

	vec2 norms0 = texture2D(tex0, txc + vec2(scroll0 / 1.0, 0.0)).rg;
	vec2 norms1 = texture2D(tex1, txc + vec2(0.0,  scroll1 / 1.0)).rg;
	vec2 norms2 = texture2D(tex2, txc + vec2(scroll2, scroll2)).rg;

	vec2 final_norms = norms0 * norms1 * norms2;
	
	gl_Position = gl_ModelViewProjectionMatrix * (vec4(0.0, final_norms.x * 16.0, 0.0, 0.0) + gl_Vertex);
}
