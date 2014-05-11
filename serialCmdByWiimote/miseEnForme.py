def miseEnForme(Vx,Vy,Omega):

	
	#Reglage de Vx
	if Vx >= 0 :
		octet0 = int('A8',16) #On force le PF vx a 1
	if Vx < 0 :
		octet0 = int('A0',16) #On force le PF vx a 0
		Vx = Vx + 127					
	
	if Vy >= 0 :
		octet0 = int('04',16) | octet0 #On force le PF vy a 1
	if Vy < 0 :
		octet0 = int('FB',16) & octet0 #On force le PF vy a 0
		Vy = Vy + 127			
	
	Omega = (Omega+64)&int('7F',16)	
	octet4 = str(chr((Vx+Vy+Omega)&127))
	octet0 = str(chr(octet0))
	octet1 = str(chr(Vx)) #On impose nos valeur de 0 a 255
	octet2 = str(chr(Vy))#On impose nos valeur de 0 a 256
	octet3 = str(chr(Omega))#On impose nos valeur de 0 a 128

	oc0_ = octet0
	oc1_ = octet1
	oc2_ = octet2
	oc3_ = octet3
	oc4_ = octet4

	cmd = oc0_ + oc1_ + oc2_ + oc3_ + oc4_

	
	return cmd
	return (octet0,octet1,octet2,octet3,octet4)
	
