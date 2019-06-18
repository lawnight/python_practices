
import os
root = r'D:\image'
cps = os.listdir(root)
cps.sort(key=lambda x:int(x[-2:]))

for i in cps:
	path = os.path.join(root,i)
	imgs = [os.path.join(path,x) for x in os.listdir(path)]
	print(imgs)	
	imgs.sort(key=lambda x:)

	print(imgs)

	strs = ['<img src="{}" />'.format(i) for i in imgs]

	with open('../html/hmate/{}'.formate(i),'w') as f:
		f.write('\r\n'.join(strs))
	