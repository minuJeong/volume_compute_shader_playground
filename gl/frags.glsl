#version 460

// written from compute shader
layout(binding=0) buffer volume_buffer
{
    vec4 volume[];
};


// matches screen/render buffer resolution
uniform uint u_width;
uniform uint u_height;

// matches volume buffer resolution
uniform uvec3 u_volumesize;

// receive camera control as uniform
uniform vec3 u_camera_pos;
uniform vec3 u_camera_dir;

// receive time as uniform
uniform float u_time;

// vertex uv
in vec2 v_uv;

// output color (screen pixel color)
out vec4 out_color;


void main()
{
    vec2 wh = vec2(u_width, u_height);
    uvec3 VV = u_volumesize;
    vec2 uv = v_uv;

    // uv.x += u_time * 1.2;
    // uv.x = fract(uv.x);

    uvec3 xyz = uvec3(uv * vec2(VV.xy), 0.0);
    xyz.z = uint(cos(u_time * 2.0) * 0.5 + 0.5);

    float debug_idx = xyz.x + xyz.y + VV.x + xyz.z * (VV.x * VV.y);

    uint i = uint(debug_idx);
    vec4 volume_data = volume[i];

    vec3 RGB = volume_data.xyz;
    // RGB = xyz / vec3(VV);

    // RGB.xy = xyz.xy / wh;

    RGB = clamp(RGB, 0.0, 1.0);
    out_color = vec4(RGB, 1.0);
}
