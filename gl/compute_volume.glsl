#version 460

layout(local_size_x=4, local_size_y=4, local_size_z=4) in;

layout(binding=0) buffer volume_buffer
{
    vec4 volume[];
};

uniform uvec3 u_volumesize;


float sphere(vec3 p, float r)
{
    return length(p) - r;
}


// customize this
float world(vec3 p)
{
    float dist_sph = sphere(p - vec3(0.5, 0.5, 0.5), 0.4);
    return dist_sph;
}


void main()
{
    uvec3 xyz = gl_LocalInvocationID.xyz + gl_WorkGroupID.xyz * gl_WorkGroupSize.xyz;
    uvec3 VV = u_volumesize;
    uint i = xyz.x + xyz.y * VV.x + xyz.z * (VV.x * VV.y);

    vec3 uvw = vec3(xyz) / vec3(u_volumesize);
    float t = world(uvw);

    float paint = smoothstep(0.02, 0.0, t);

    volume[i] = vec4(uvw.xy, paint, 1.0);
}
