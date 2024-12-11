# Data structure
registerFiles = {
	"x0" : 0,
	"x1" : 0,
    "x2" : 0,
    "x3" : 0,
	"x4" : 0,
    "x5" : 0,
    "x6" : 0,
	"x7" : 0,
    "x8" : 0,
    "x9" : 0,
	"x10" : 0,
    "x11" : 0,
    "x12" : 0,
	"x13" : 0,
    "x14" : 0,
    "x15" : 0,
	"x16" : 0,
    "x17" : 0,
    "x18" : 0,
	"x19" : 0,
    "x20" : 0,
    "x21" : 0,
	"x22" : 0,
    "x23" : 0,
    "x24" : 0,
    "x25" : 0,
    "x26" : 0,
	"x27" : 0,
    "x28" : 0,
    "x29" : 0,
	"x30" : 0,
	"x31" : 0
}

dict dataMemory{

}

pc = 0

def executeR(funct3, funct7, rd, rs1, rs2):
	if funct3 == "000":
		if funct7 == "00":				
			registerFiles[rd] = registerFiles[rs1] + registerFiles[rs2]
		else:
			registerFiles[rd] = registerFiles[rs1] - registerFiles[rs2]
	elif funct3 == "001":          
		registerFiles[rd] = registerFiles[rs1] & registerFiles[rs2]
	elif funct3 == "002":          
		registerFiles[rd] = registerFiles[rs1] & registerFiles[rs2]
	elif funct3 == "003":          
		registerFiles[rd] = registerFiles[rs1] & registerFiles[rs2]
	elif funct3 == "004":          
		registerFiles[rd] = registerFiles[rs1] & registerFiles[rs2]
	elif funct3 == "005":          
		registerFiles[rd] = registerFiles[rs1] & registerFiles[rs2]
	elif funct3 == "006":          
		registerFiles[rd] = registerFiles[rs1] & registerFiles[rs2]
	elif funct3 == "007":          
		registerFiles[rd] = registerFiles[rs1] & registerFiles[rs2]


def instDecoder(inst):
	
endfunc

with open 

for i, line in enumerate(input):	// fetch
	opcode, func3, fun7, rs1, rs2, ...decode		// decode
	// Execution
	if format == R executeR(opcode, rd, rs1, rs2)
	elif format == I executeI()
	store > registerFiles/dataMemory
	pc += 4
end

sw x0 , 0xFFC0(x0)
sw x1, 0xFFC4(x0)
..
sw x31 ()


print(registerFiles)
print(dataMemory)