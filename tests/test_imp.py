import sys
sys.path.append("../build/lib/")
import lprecmods.lpTransform as lpTransform
import matplotlib.pyplot as plt
from numpy import *
import struct

N=2016
Nproj=1800
Nslices=1
filter_type='hamming'
pad=True
cor=N/2-4

fid = open('./data/Rimp', 'rb')
R=float32(reshape(struct.unpack(Nproj*N*'f',fid.read(Nproj*N*4)),[Nslices,N,Nproj]))

clpthandle=lpTransform.lpTransform(N,Nproj,Nslices,filter_type,pad)
clpthandle.precompute()

frec=clpthandle.adj(R,cor);

plt.subplot(1,2,1)
plt.imshow(R[0,:,:])
plt.colorbar()
plt.subplot(1,2,2)
plt.imshow(frec[0,:,:])
plt.colorbar()
plt.show()
