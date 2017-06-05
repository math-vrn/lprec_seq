import sys
sys.path.append("../build/lib/")

import lprecmods.lpTransform as lpTransform
import matplotlib.pyplot as plt
from numpy import *
import struct
N=256
Nproj=64
Nslices=1
filter_type='None'
pad=True
cor=N/2

fid = open('./data/fbub', 'rb')
f=float32(reshape(struct.unpack(N*N*'f',fid.read(N*N*4)),[Nslices,N,N]))

fid = open('./data/Rbub', 'rb')
R=float32(reshape(struct.unpack(Nproj*N*'f',fid.read(Nproj*N*4)),[Nslices,N,Nproj]))

clpthandle=lpTransform.lpTransform(N,Nproj,Nslices,filter_type,pad)

clpthandle.precompute()

frec=clpthandle.adj(R,cor);

plt.subplot(1,3,1)
plt.imshow(f[0,:,:])
plt.colorbar()
plt.subplot(1,3,2)
plt.imshow(frec[0,:,:])
plt.colorbar()
plt.subplot(1,3,3)
plt.imshow(abs(frec[0,:,:]-f[0,:,:]))
plt.colorbar()


plt.show()
