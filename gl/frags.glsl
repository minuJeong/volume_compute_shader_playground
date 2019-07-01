#version 460

layout(binding=0) buffer volume_buffer
{
    vec4 volume[];
};

uniform uint u_width;
uniform uint u_height;
uniform uvec3 u_volumesize;
uniform vec3 u_camera_pos;
uniform vec3 u_camera_dir;
uniform float u_time;

in vec2 v_uv;
out vec4 out_color;


void main()
{
    vec2 wh = vec2(u_width, u_height);
    uvec3 VV = u_volumesize;
    vec2 uv = v_uv;

    uvec3 xyz = uvec3(uv * vec2(VV.xy), 0.0);
    xyz.z = uint(cos(u_time * 2.0) * 0.5 + 0.5);


    float debug_idx = xyz.x + xyz.y + VV.x + xyz.z * (VV.x * VV.y);

    uint i = uint(debug_idx);
    vec4 volume_data = volume[i];

    vec3 RGB = volume_data.xyz;
    RGB = xyz / vec3(VV);

    // RGB.xy = xyz.xy / wh;

    RGB = clamp(RGB, 0.0, 1.0);
    out_color = vec4(RGB, 1.0);
}
