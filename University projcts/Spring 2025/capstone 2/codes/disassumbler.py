import os
import lief
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
import pefile

# Set input and output paths
file_path = "C:\\Users\\User\\Downloads\\SteamSetup.exe" 
output_path = os.path.join("C:\\Users\\User\\Downloads", "disassembly_output1.asm")

def print_user_file_magic(file_path, num_bytes=8, out_lines=[]):
    try:
        with open(file_path, "rb") as f:
            magic = f.read(num_bytes)
            line = f"[+] Magic number of user file ({file_path}): {magic.hex()}"
            print(line)
            out_lines.append(line)
    except Exception as e:
        line = f"[!] Error reading file: {e}"
        print(line)
        out_lines.append(line)

def is_elf(file_path):
    with open(file_path, "rb") as f:
        return f.read(4) == b'\x7fELF'

def is_pe(file_path):
    with open(file_path, "rb") as f:
        return f.read(2) == b'MZ'

def disassumble_x86_64(code, addr, out_lines):
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    md.detail = True
    for instr in md.disasm(code, addr):
        line = f"0x{instr.address:x}: {instr.mnemonic} {instr.op_str}"
        out_lines.append(line)

def disassemble_elf(file_path, out_lines):
    try:
        with open(file_path, "rb") as f:
            elf = ELFFile(f)
            text_section = elf.get_section_by_name(".text")
            if not text_section:
                out_lines.append("[!] No .text section in pyelftools.")
                raise ELFError("Missing .text")
            code = text_section.data()
            addr = text_section.header["sh_addr"]
            out_lines.append("[+] Disassembling .text via pyelftools")
            disassumble_x86_64(code, addr, out_lines)
    except Exception as e:
        out_lines.append(f"[!] pyelftools failed: {e}")
        try:
            binary = lief.parse(file_path)
            text = binary.get_section(".text")
            if not text:
                out_lines.append("[!] No .text section found using LIEF either.")
                return
            code = bytes(text.content)
            addr = text.virtual_address
            out_lines.append("[+] Disassembling .text via LIEF fallback")
            disassumble_x86_64(code, addr, out_lines)
        except Exception as lief_error:
            out_lines.append(f"[!] LIEF parsing failed: {lief_error}")

def disassemble_pe(file_path, out_lines):
    try:
        pe = pefile.PE(file_path)
        text_section = next((s for s in pe.sections if s.Name.startswith(b".text")), None)
        if not text_section:
            out_lines.append("No .text section found in the PE binary (pefile)")
            raise ValueError("Missing .text section")
        
        raw = text_section.get_data()
        i = len(raw) - 1
        while i >= 0 and raw[i] in (0x00, 0x90):
            i -= 1
        code = raw[:i + 1]
        addr = text_section.VirtualAddress + pe.OPTIONAL_HEADER.ImageBase
        out_lines.append(f"[+] Disassembling PE .text section via pefile (Base Address: 0x{addr:x})")
        disassumble_x86_64(code, addr, out_lines)

    except Exception as e:
        out_lines.append(f"[!] pefile failed: {e}")
        # Try LIEF fallback
        try:
            binary = lief.parse(file_path)
            section = binary.get_section(".text")
            if not section:
                out_lines.append("[!] No .text section found in PE binary via LIEF.")
                return
            code = bytes(section.content)
            addr = section.virtual_address
            out_lines.append(f"[+] Disassembling PE .text section via LIEF (Base Address: 0x{addr:x})")
            disassumble_x86_64(code, addr, out_lines)
        except Exception as lief_error:
            out_lines.append(f"[!] LIEF fallback failed: {lief_error}")


def disassemble_raw(file_path, out_lines):
    try:
        with open(file_path, "rb") as f:
            code = f.read()
        out_lines.append("[+] Disassembling raw .bin file")
        disassumble_x86_64(code, 0x0, out_lines)
    except Exception as e:
        out_lines.append(f"[!] Failed to disassemble raw binary: {e}")

def disassemble_file(file_path):
    out_lines = []
    print_user_file_magic(file_path, out_lines=out_lines)

    if is_elf(file_path):
        out_lines.append(f"[+] Detected ELF binary: {file_path}")
        disassemble_elf(file_path, out_lines)
    elif is_pe(file_path):
        out_lines.append(f"[+] Detected PE (Windows EXE) binary: {file_path}")
        disassemble_pe(file_path, out_lines)
    else:
        out_lines.append("[!] Unsupported format — trying raw disassembly...")
        disassemble_raw(file_path, out_lines)

    # Filter metadata out of final saved output
    disassembly_only = [line for line in out_lines if not line.startswith("[+") and not line.startswith("[!]")]

    with open(output_path, "w") as f:
        f.write("\n".join(disassembly_only))

    print(f"\n✅ Disassembly saved to: {output_path}")

# Run
if __name__ == "__main__":
    disassemble_file(file_path)
