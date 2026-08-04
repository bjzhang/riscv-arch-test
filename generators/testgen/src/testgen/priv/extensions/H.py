##################################
# priv/H.py
#
# H hypervisor privileged extension test generator.
# SPDX-License-Identifier: Apache-2.0
##################################

"""H hypervisor privileged extension test generator."""

from testgen.asm.csr import csr_access_test, csr_walk_test, gen_csr_read_sigupd, gen_csr_write_sigupd
from testgen.asm.helpers import comment_banner, write_sigupd
from testgen.constants import INDENT
from testgen.data.state import TestData
from testgen.data.test_chunk import TestChunk
from testgen.priv.registry import add_priv_test_generator

COVERGROUP = "H_cg"

MACHINE_H_CSRS = [("mtval2", None), ("mtinst", None)]
HS_H_CSRS = [
    ("hstatus", None),
    ("hedeleg", None),
    ("hideleg", None),
    ("hie", None),
    ("hcounteren", None),
    ("hgeie", None),
    ("henvcfg", None),
    ("htval", None),
    ("hip", None),
    ("hvip", None),
    ("htinst", None),
    ("hgatp", None),
    ("hgeip", None),
    ("htimedelta", None),
]
HS_H_CSRS_RV32 = [("hedelegh", None), ("htimedeltah", None), ("henvcfgh", None)]
VS_H_CSRS = [
    ("vsstatus", None),
    ("vsie", None),
    ("vstvec", None),
    ("vsscratch", None),
    ("vsepc", None),
    ("vscause", None),
    ("vstval", None),
    ("vsip", None),
    ("vsatp", None),
]
S_REPLICA_CSRS = ["sstatus", "sie", "stvec", "sscratch", "sepc", "scause", "stval", "sip", "satp"]
S_NONREPLICA_CSRS = ["scounteren", "senvcfg", "scountinhibit"]
HIGH_HALF_CSRS = ["hedelegh", "htimedeltah", "henvcfgh", "vstimecmph"]


def _goto_mode(mode: str) -> str:
    return f"RVTEST_TSBI_GOTO_{mode}MODE"


def _csrr(reg: int, csr: str) -> str:
    return f"csrr x{reg}, {csr}"


def _csrw(csr: str, reg: int) -> str:
    return f"csrw {csr}, x{reg}"


def _csrs(csr: str, reg: int) -> str:
    return f"csrs {csr}, x{reg}"


def _csrc(csr: str, reg: int) -> str:
    return f"csrc {csr}, x{reg}"


def _generate_hcsr_access_tests(test_data: TestData) -> list[str]:
    """Generate CSR access tests for machine, HS, and VS H-extension CSRs."""
    lines = [comment_banner("cp_hcsr_access_m", "M-mode access to machine H-extension CSRs")]
    for csr in MACHINE_H_CSRS:
        lines.extend(csr_access_test(test_data, csr, COVERGROUP, "cp_hcsr_access_m_m"))

    lines.append(comment_banner("cp_hcsr_access_hs", "M-mode access to HS H-extension CSRs"))
    for csr in HS_H_CSRS:
        lines.extend(csr_access_test(test_data, csr, COVERGROUP, "cp_hcsr_access_hs_m"))

    lines.append(comment_banner("cp_hcsr_access_vs", "M-mode access to VS H-extension CSRs"))
    for csr in VS_H_CSRS:
        lines.extend(csr_access_test(test_data, csr, COVERGROUP, "cp_hcsr_access_vs_m"))

    lines.extend(["", "#if __riscv_xlen == 32"])
    for csr in HS_H_CSRS_RV32:
        lines.extend(csr_access_test(test_data, csr, COVERGROUP, "cp_hcsr_access_hs_m_rv32"))
    lines.append("#endif")

    lines.extend(["", _goto_mode("S"), comment_banner("cp_hcsr_access_hs", "HS-mode access to HS H-extension CSRs")])
    for csr in HS_H_CSRS:
        lines.extend(csr_access_test(test_data, csr, COVERGROUP, "cp_hcsr_access_hs_hs"))

    lines.append(comment_banner("cp_hcsr_access_vs", "HS-mode access to VS H-extension CSRs"))
    for csr in VS_H_CSRS:
        lines.extend(csr_access_test(test_data, csr, COVERGROUP, "cp_hcsr_access_vs_hs"))

    lines.extend(["", "#if __riscv_xlen == 32"])
    for csr in HS_H_CSRS_RV32:
        lines.extend(csr_access_test(test_data, csr, COVERGROUP, "cp_hcsr_access_hs_hs_rv32"))
    lines.extend(["#endif", _goto_mode("M")])
    return lines


def _generate_hcsr_walk_tests(test_data: TestData) -> list[str]:
    """Generate CSR walking-bit tests for H-extension CSRs."""
    lines = [comment_banner("cp_hcsrwalk_m", "Walk bits in machine H-extension CSRs from M-mode")]
    for csr in MACHINE_H_CSRS:
        lines.extend(csr_walk_test(test_data, csr, COVERGROUP, "cp_hcsrwalk_m_m"))

    lines.append(comment_banner("cp_hcsrwalk_hs", "Walk bits in HS H-extension CSRs"))
    for csr in HS_H_CSRS:
        if csr[0] == "hstatus":
            continue
        lines.extend(csr_walk_test(test_data, csr, COVERGROUP, "cp_hcsrwalk_hs_m"))

    lines.append(comment_banner("cp_hcsrwalk_vs", "Walk bits in VS H-extension CSRs"))
    for csr in VS_H_CSRS:
        if csr[0] == "vsstatus":
            continue
        lines.extend(csr_walk_test(test_data, csr, COVERGROUP, "cp_hcsrwalk_vs_m"))

    lines.extend(["", "#if __riscv_xlen == 32"])
    for csr in HS_H_CSRS_RV32:
        lines.extend(csr_walk_test(test_data, csr, COVERGROUP, "cp_hcsrwalk_hs_m_rv32"))
    lines.append("#endif")

    lines.extend(["", _goto_mode("S"), comment_banner("cp_hcsrwalk_hs", "Walk bits in HS H-extension CSRs")])
    for csr in HS_H_CSRS:
        if csr[0] == "hstatus":
            continue
        lines.extend(csr_walk_test(test_data, csr, COVERGROUP, "cp_hcsrwalk_hs_hs"))

    lines.append(comment_banner("cp_hcsrwalk_vs", "Walk bits in VS H-extension CSRs"))
    for csr in VS_H_CSRS:
        if csr[0] == "vsstatus":
            continue
        lines.extend(csr_walk_test(test_data, csr, COVERGROUP, "cp_hcsrwalk_vs_hs"))

    lines.extend(["", "#if __riscv_xlen == 32"])
    for csr in HS_H_CSRS_RV32:
        lines.extend(csr_walk_test(test_data, csr, COVERGROUP, "cp_hcsrwalk_hs_hs_rv32"))
    lines.append("#endif")
    return lines


def _generate_replica_tests(test_data: TestData) -> list[str]:
    """Generate S/VS replica and non-replica CSR substitution tests."""
    value_reg, scratch = test_data.int_regs.get_registers(2)
    lines = [
        comment_banner("cp_replica_v0", "S CSRs and VS replicas are independent when V=0"),
        f"LI(x{value_reg}, 0x5a5a)",
    ]
    for csr in S_REPLICA_CSRS:
        lines.extend(
            [
                "",
                test_data.add_testcase(f"v0_{csr}", "cp_replica_v0", COVERGROUP),
                _csrw(csr, value_reg),
                gen_csr_read_sigupd(value_reg, (csr, None), test_data),
            ]
        )

    lines.extend(["", _goto_mode("VS"), comment_banner("cp_nonreplica_v1", "S CSRs without VS replicas remain accessible with V=1")])
    for csr in S_NONREPLICA_CSRS:
        lines.extend(
            [
                "",
                test_data.add_testcase(f"v1_{csr}", "cp_nonreplica_v1", COVERGROUP),
                _csrr(value_reg, csr),
                write_sigupd(value_reg, test_data),
            ]
        )
    lines.append(_goto_mode("M"))
    test_data.int_regs.return_registers([value_reg])
    return lines


def _generate_special_csr_field_tests(test_data: TestData) -> list[str]:
    """Generate H-specific CSR field tests."""
    value_reg, mask_reg, save_reg = test_data.int_regs.get_registers(3)
    lines = [
        comment_banner("cp_mtvala", "mtval must not be read-only zero"),
        _csrr(save_reg, "mtval"),
        f"LI(x{value_reg}, -1)",
        test_data.add_testcase("write_ones", "cp_mtvala", COVERGROUP),
        gen_csr_write_sigupd(value_reg, "mtval", test_data),
        _csrw("mtval", save_reg),
        "",
        comment_banner("cp_hstatus_vgein", "Write representative hstatus.VGEIN values"),
        _csrr(save_reg, "hstatus"),
    ]
    for value in (0, 1, 2, 63):
        lines.extend(
            [
                "",
                f"LI(x{value_reg}, {value << 12})",
                f"LI(x{mask_reg}, 0x3f000)",
                f"not x{mask_reg}, x{mask_reg}",
                f"and x{value_reg}, x{value_reg}, x{mask_reg}",
                f"or x{value_reg}, x{value_reg}, x{save_reg}",
                test_data.add_testcase(f"vgein_{value}", "cp_hstatus_vgein", COVERGROUP),
                gen_csr_write_sigupd(value_reg, "hstatus", test_data),
            ]
        )
    lines.extend([_csrw("hstatus", save_reg), "", comment_banner("cp_vscause_write", "Write WLRL vscause interrupt and exception encodings")])
    for interrupt in (0, 1):
        for cause in (0, 1, 2, 15, 22, 63):
            label = f"i{interrupt}_cause{cause}"
            lines.extend(
                [
                    "",
                    f"LI(x{value_reg}, {cause})",
                    f"#if __riscv_xlen == 64" if interrupt else "#if 1",
                    f"SET_MSB(x{mask_reg})" if interrupt else f"LI(x{mask_reg}, 0)",
                    f"or x{value_reg}, x{value_reg}, x{mask_reg}",
                    test_data.add_testcase(label, "cp_vscause_write", COVERGROUP),
                    gen_csr_write_sigupd(value_reg, "vscause", test_data),
                    "#endif",
                ]
            )

    lines.append(comment_banner("cp_vsstatus_sd_write", "Cross vsstatus FS/VS against SD"))
    for fs in range(4):
        for vs_field in range(4):
            fields = (fs << 13) | (vs_field << 9)
            lines.extend(
                [
                    "",
                    f"LI(x{value_reg}, 0x{fields:x})",
                    test_data.add_testcase(f"fs{fs}_vs{vs_field}", "cp_vsstatus_sd_write", COVERGROUP),
                    gen_csr_write_sigupd(value_reg, "vsstatus", test_data),
                ]
            )
    test_data.int_regs.return_registers([value_reg, mask_reg, save_reg])
    return lines


def _generate_privilege_trap_tests(test_data: TestData) -> list[str]:
    """Generate CSR and instruction permission trap tests."""
    reg = test_data.int_regs.get_register()
    lines = [comment_banner("cp_hcsr_inaccessible", "Machine H CSRs are inaccessible below M-mode")]
    for mode in ("S", "VS", "U", "VU"):
        lines.append(_goto_mode(mode))
        for csr, _mask in MACHINE_H_CSRS:
            lines.extend(["", test_data.add_testcase(f"{mode.lower()}_{csr}", "cp_hcsr_inaccessible", COVERGROUP), _csrr(reg, csr)])

    lines.extend([_goto_mode("VS"), comment_banner("cp_hcsr_virtualinstructionfault", "HS and VS CSR direct accesses trap virtually when V=1")])
    for csr, _mask in HS_H_CSRS + VS_H_CSRS:
        lines.extend(["", test_data.add_testcase(f"vs_{csr}", "cp_hcsr_virtualinstructionfault", COVERGROUP), _csrr(reg, csr)])

    lines.extend(["", "#if __riscv_xlen == 64", comment_banner("cp_illegalupper", "High-half H CSRs are illegal when XLEN is greater than 32")])
    for csr in HIGH_HALF_CSRS:
        lines.extend(["", test_data.add_testcase(csr, "cp_illegalupper", COVERGROUP), _csrr(reg, csr)])
    lines.extend(["#endif", "", comment_banner("cp_scsr_u_vu", "U/VU supervisor CSR access traps")])
    for mode in ("U", "VU"):
        lines.append(_goto_mode(mode))
        for csr in S_REPLICA_CSRS + S_NONREPLICA_CSRS:
            lines.extend(["", test_data.add_testcase(f"{mode.lower()}_{csr}", "cp_scsr_u_vu", COVERGROUP), _csrr(reg, csr)])
    lines.append(_goto_mode("M"))
    test_data.int_regs.return_registers([reg])
    return lines


def _generate_tvm_tests(test_data: TestData) -> list[str]:
    """Generate TVM and VTVM trap tests for hgatp/satp and fences."""
    reg, save_status, save_hstatus = test_data.int_regs.get_registers(3)
    lines = [
        comment_banner("cp_tvm_hgatp", "mstatus.TVM controls HS access to hgatp"),
        _csrr(save_status, "mstatus"),
        _csrr(save_hstatus, "hstatus"),
    ]
    for tvm in (0, 1):
        lines.extend(
            [
                "",
                f"LI(x{reg}, {tvm << 20})",
                _csrs("mstatus", reg) if tvm else _csrc("mstatus", reg),
                _goto_mode("S"),
                test_data.add_testcase(f"hgatp_tvm{tvm}", "cp_tvm_hgatp", COVERGROUP),
                _csrr(reg, "hgatp"),
                _goto_mode("M"),
            ]
        )

    lines.append(comment_banner("cp_tvm_vsatp", "hstatus.VTVM controls VS access to satp"))
    for tvm in (0, 1):
        for vtvm in (0, 1):
            lines.extend(
                [
                    "",
                    f"LI(x{reg}, {tvm << 20})",
                    _csrs("mstatus", reg) if tvm else _csrc("mstatus", reg),
                    f"LI(x{reg}, {vtvm << 20})",
                    _csrs("hstatus", reg) if vtvm else _csrc("hstatus", reg),
                    _goto_mode("VS"),
                    test_data.add_testcase(f"satp_tvm{tvm}_vtvm{vtvm}", "cp_tvm_vsatp", COVERGROUP),
                    _csrr(reg, "satp"),
                    _goto_mode("M"),
                ]
            )
    lines.extend([_csrw("mstatus", save_status), _csrw("hstatus", save_hstatus)])
    test_data.int_regs.return_registers([reg, save_status, save_hstatus])
    return lines


def _generate_h_load_store_tests(test_data: TestData) -> list[str]:
    """Generate HLV, HLVX, and HSV opcode coverage tests."""
    addr_reg, value_reg = test_data.int_regs.get_registers(2)
    lines = [
        comment_banner("cp_hlv", "Execute HLV loads from scratch guest address"),
        f"LA(x{addr_reg}, scratch)",
    ]
    for mode in ("M", "S", "U"):
        lines.append(_goto_mode(mode))
        if mode == "U":
            lines.extend([f"LI(x{value_reg}, 0x200)", _csrs("hstatus", value_reg)])
        for instr in ("hlv.b", "hlv.bu", "hlv.h", "hlv.hu", "hlv.w"):
            lines.extend(["", test_data.add_testcase(f"{mode.lower()}_{instr.replace('.', '_')}", "cp_hlv", COVERGROUP), f"{instr} x{value_reg}, 0(x{addr_reg})", "nop", write_sigupd(value_reg, test_data)])
        lines.extend(["#if __riscv_xlen == 64", test_data.add_testcase(f"{mode.lower()}_hlv_wu", "cp_hlv", COVERGROUP), f"hlv.wu x{value_reg}, 0(x{addr_reg})", "nop", write_sigupd(value_reg, test_data), test_data.add_testcase(f"{mode.lower()}_hlv_d", "cp_hlv", COVERGROUP), f"hlv.d x{value_reg}, 0(x{addr_reg})", "nop", write_sigupd(value_reg, test_data), "#endif"])

    lines.append(comment_banner("cp_hlvx", "Execute HLVX loads from scratch guest address"))
    for mode in ("M", "S", "U"):
        lines.append(_goto_mode(mode))
        for instr in ("hlvx.hu", "hlvx.wu"):
            lines.extend(["", test_data.add_testcase(f"{mode.lower()}_{instr.replace('.', '_')}", "cp_hlvx", COVERGROUP), f"{instr} x{value_reg}, 0(x{addr_reg})", "nop", write_sigupd(value_reg, test_data)])

    lines.append(comment_banner("cp_hsv", "Execute HSV stores to scratch guest address"))
    for mode in ("M", "S", "U"):
        lines.append(_goto_mode(mode))
        for instr in ("hsv.b", "hsv.h", "hsv.w"):
            lines.extend(["", f"LI(x{value_reg}, 0x12345678)", test_data.add_testcase(f"{mode.lower()}_{instr.replace('.', '_')}", "cp_hsv", COVERGROUP), f"{instr} x{value_reg}, 0(x{addr_reg})", "nop", write_sigupd(value_reg, test_data)])
        lines.extend(["#if __riscv_xlen == 64", f"LI(x{value_reg}, 0x123456789abcdef0)", test_data.add_testcase(f"{mode.lower()}_hsv_d", "cp_hsv", COVERGROUP), f"hsv.d x{value_reg}, 0(x{addr_reg})", "nop", write_sigupd(value_reg, test_data), "#endif"])
    lines.append(_goto_mode("M"))
    test_data.int_regs.return_registers([addr_reg, value_reg])
    return lines


def _generate_fence_tests(test_data: TestData) -> list[str]:
    """Generate HFENCE and SFENCE instruction coverage tests."""
    reg, save_status, save_hstatus = test_data.int_regs.get_registers(3)
    lines = [
        comment_banner("cp_hfence", "Execute HFENCE.VVMA/GVMA across mode and TVM/VTVM state"),
        _csrr(save_status, "mstatus"),
        _csrr(save_hstatus, "hstatus"),
    ]
    for mode in ("M", "S"):
        for tvm in (0, 1):
            for vtvm in (0, 1):
                lines.extend(["", f"LI(x{reg}, {tvm << 20})", _csrs("mstatus", reg) if tvm else _csrc("mstatus", reg), f"LI(x{reg}, {vtvm << 20})", _csrs("hstatus", reg) if vtvm else _csrc("hstatus", reg), _goto_mode(mode), test_data.add_testcase(f"{mode.lower()}_vvma_tvm{tvm}_vtvm{vtvm}", "cp_hfence", COVERGROUP), "hfence.vvma", "nop", test_data.add_testcase(f"{mode.lower()}_gvma_tvm{tvm}_vtvm{vtvm}", "cp_hfence", COVERGROUP), "hfence.gvma", "nop"])

    lines.append(comment_banner("cp_sfence", "Execute SFENCE.VMA across mode and TVM/VTVM state"))
    for mode in ("M", "S", "VS"):
        for tvm in (0, 1):
            for vtvm in (0, 1):
                lines.extend(["", f"LI(x{reg}, {tvm << 20})", _csrs("mstatus", reg) if tvm else _csrc("mstatus", reg), f"LI(x{reg}, {vtvm << 20})", _csrs("hstatus", reg) if vtvm else _csrc("hstatus", reg), _goto_mode(mode), test_data.add_testcase(f"{mode.lower()}_sfence_tvm{tvm}_vtvm{vtvm}", "cp_sfence", COVERGROUP), "sfence.vma", "nop", _goto_mode("M")])
    lines.extend([_csrw("mstatus", save_status), _csrw("hstatus", save_hstatus)])
    test_data.int_regs.return_registers([reg, save_status, save_hstatus])
    return lines


def _generate_ret_tests(test_data: TestData) -> list[str]:
    """Generate H-related MRET/SRET virtualization return tests."""
    reg, retaddr, save_status, save_hstatus = test_data.int_regs.get_registers(4)
    lines = [
        comment_banner("cp_mret_m", "MRET uses mstatus.MPV and MPP"),
        _csrr(save_status, "mstatus"),
        _csrr(save_hstatus, "hstatus"),
    ]
    for mpp in (0, 1, 3):
        for mpv in (0, 1):
            lines.extend(["", f"LA(x{retaddr}, 1f)", _csrw("mepc", retaddr), f"LI(x{reg}, {(mpp << 11) | (mpv << 17)})", _csrs("mstatus", reg), test_data.add_testcase(f"mpp{mpp}_mpv{mpv}", "cp_mret_m", COVERGROUP), "mret", f"{INDENT}# mret should branch to label 1", "nop", "1:", write_sigupd(reg, test_data), _goto_mode("M")])

    lines.append(comment_banner("cp_mret_illegal", "MRET is unavailable below M-mode"))
    for mode in ("S", "VS", "VU"):
        lines.extend(["", _goto_mode(mode), test_data.add_testcase(mode.lower(), "cp_mret_illegal", COVERGROUP), "mret", "nop", _goto_mode("M")])

    lines.append(comment_banner("cp_sret_illegal", "SRET is unavailable in VU-mode"))
    lines.extend([_goto_mode("VU"), test_data.add_testcase("vu", "cp_sret_illegal", COVERGROUP), "sret", "nop", _goto_mode("M")])

    lines.append(comment_banner("cp_sret_m", "SRET from M-mode uses SPP, SPV, and SPIE state"))
    for spp in (0, 1):
        for spv in (0, 1):
            for spie in (0, 1):
                lines.extend(["", f"LA(x{retaddr}, 2f)", _csrw("sepc", retaddr), f"LI(x{reg}, {(spp << 8) | (spie << 5)})", _csrs("sstatus", reg), f"LI(x{reg}, {spv << 7})", _csrs("hstatus", reg), test_data.add_testcase(f"spp{spp}_spv{spv}_spie{spie}", "cp_sret_m", COVERGROUP), "sret", "nop", "2:", write_sigupd(reg, test_data), _goto_mode("M")])

    lines.append(comment_banner("cp_sret_hs", "SRET from HS-mode uses SPP, SPIE, and hstatus.SPV"))
    for spp in (0, 1):
        for spv in (0, 1):
            for spie in (0, 1):
                lines.extend(["", _goto_mode("S"), f"LA(x{retaddr}, 3f)", _csrw("sepc", retaddr), f"LI(x{reg}, {(spp << 8) | (spie << 5)})", _csrs("sstatus", reg), f"LI(x{reg}, {spv << 7})", _csrs("hstatus", reg), test_data.add_testcase(f"spp{spp}_spv{spv}_spie{spie}", "cp_sret_hs", COVERGROUP), "sret", "nop", "3:", write_sigupd(reg, test_data), _goto_mode("M")])

    lines.append(comment_banner("cp_sret_vs", "SRET from VS-mode uses VS status unless VTSR traps"))
    for spp in (0, 1):
        for spie in (0, 1):
            for vtsr in (0, 1):
                lines.extend(["", f"LI(x{reg}, {vtsr << 22})", _csrs("hstatus", reg) if vtsr else _csrc("hstatus", reg), _goto_mode("VS"), f"LA(x{retaddr}, 4f)", _csrw("vsepc", retaddr), f"LI(x{reg}, {(spp << 8) | (spie << 5)})", _csrs("vsstatus", reg), test_data.add_testcase(f"spp{spp}_spie{spie}_vtsr{vtsr}", "cp_sret_vs", COVERGROUP), "sret", "nop", "4:", write_sigupd(reg, test_data), _goto_mode("M")])
    lines.extend([_csrw("mstatus", save_status), _csrw("hstatus", save_hstatus)])
    test_data.int_regs.return_registers([reg, retaddr, save_status, save_hstatus])
    return lines


@add_priv_test_generator(
    "H",
    extra_defines=["#define RVTEST_ENABLE_H", "#define RVTEST_HYPERVISOR"],
    required_extensions=["H", "Zicsr"],
    march_extensions=["H", "Zicsr"],
)
def make_h(test_data: TestData) -> list[TestChunk]:
    """Generate tests for the H hypervisor CSRs and instructions suite."""
    test_chunks: list[TestChunk] = []

    tc = test_data.begin_test_chunk("csr_access")
    tc.code.extend(_generate_hcsr_access_tests(test_data))
    tc.code.extend(_generate_hcsr_walk_tests(test_data))
    tc.code.extend(_generate_replica_tests(test_data))
    tc.code.extend(_generate_special_csr_field_tests(test_data))
    test_chunks.append(test_data.end_test_chunk())

    tc = test_data.begin_test_chunk("csr_traps")
    tc.code.extend(_generate_privilege_trap_tests(test_data))
    tc.code.extend(_generate_tvm_tests(test_data))
    test_chunks.append(test_data.end_test_chunk())

    tc = test_data.begin_test_chunk("instructions")
    tc.code.extend(_generate_h_load_store_tests(test_data))
    tc.code.extend(_generate_fence_tests(test_data))
    tc.code.extend(_generate_ret_tests(test_data))
    test_chunks.append(test_data.end_test_chunk())

    return test_chunks

# --- Workspace H generator override matching unity_test/H/coverpoints/priv/H_coverage.svh ---

M_H_ACCESS_CSRS = [
    ("mtval2", None),
    ("mtinst", None),
    ("hstatus", None),
    ("hedeleg", None),
    ("hideleg", None),
    ("hie", None),
    ("htimedelta", None),
    ("hcounteren", None),
    ("hgeie", None),
    ("henvcfg", None),
    ("htval", None),
    ("hip", None),
    ("hvip", None),
    ("htinst", None),
    ("hgatp", None),
    ("hgeip", None),
]

HS_H_ACCESS_CSRS = [
    ("hstatus", None),
    ("hedeleg", None),
    ("hideleg", None),
    ("hie", None),
    ("htimedelta", None),
    ("hcounteren", None),
    ("hgeie", None),
    ("henvcfg", None),
    ("htval", None),
    ("hip", None),
    ("hvip", None),
    ("htinst", None),
    ("hgatp", None),
    ("hgeip", None),
]

VS_H_ACCESS_CSRS = [
    ("vsstatus", None),
    ("vsie", None),
    ("vstvec", None),
    ("vsscratch", None),
    ("vsepc", None),
    ("vscause", None),
    ("vstval", None),
    ("vsip", None),
    ("vsatp", None),
]

HS_WALK_CSRS = [csr for csr in HS_H_ACCESS_CSRS if csr[0] != "hstatus"] + VS_H_ACCESS_CSRS[:-1]
M_WALK_CSRS = [csr for csr in M_H_ACCESS_CSRS if csr[0] not in {"hstatus"}]

S_REPLICA_CSRS = ["sstatus", "sie", "stvec", "sscratch", "sepc", "scause", "stval", "sip", "satp"]
S_NONREPLICA_CSRS = ["scounteren", "senvcfg", "scountinhibit"]
HIGH_HALF_CSRS = ["hedelegh", "htimedeltah", "henvcfgh", "vstimecmph"]


def _emit_trap_accesses(
    test_data: TestData,
    covergroup: str,
    coverpoint: str,
    mode: str,
    csrs: list[str],
    label_prefix: str,
) -> list[str]:
    lines: list[str] = [comment_banner(coverpoint, f"{label_prefix} from {mode}-mode")]
    reg, scratch = test_data.int_regs.get_registers(2)
    lines.append(_goto_mode(mode))
    lines.append(f"LI(x{reg}, -1)")
    for csr in csrs:
        for op in ("csrrw", "csrrs", "csrrc", "csrr"):
            label = f"{mode.lower()}_{csr}_{op}"
            lines.append(test_data.add_testcase(label, coverpoint, covergroup))
            if op == "csrr":
                lines.append(f"csrr x{scratch}, {csr}")
            else:
                lines.append(f"{op} x{scratch}, {csr}, x{reg}")
            lines.append("nop")
    lines.append(_goto_mode("M"))
    test_data.int_regs.return_registers([reg, scratch])
    return lines


def _generate_workspace_h_csr_tests(test_data: TestData) -> list[str]:
    lines: list[str] = []

    lines.append(comment_banner("cp_hcsr_access", "M-mode access to all H-extension CSRs"))
    for csr in M_H_ACCESS_CSRS:
        lines.extend(csr_access_test(test_data, csr, "H_mcsr_cg", "cp_hcsr_access"))

    lines.append(comment_banner("cp_hcsrwalk", "M-mode walk of H-extension CSRs"))
    for csr in M_WALK_CSRS:
        lines.extend(csr_walk_test(test_data, csr, "H_mcsr_cg", "cp_hcsrwalk"))

    lines.append(comment_banner("cp_replica", "M-mode write/read of S and VS CSRs"))
    value_reg, scratch = test_data.int_regs.get_registers(2)
    lines.append(f"LI(x{value_reg}, 0x5a5a5a5a)")
    for csr in S_REPLICA_CSRS:
        lines.extend([
            "",
            test_data.add_testcase(f"m_{csr}", "cp_replica", "H_mcsr_cg"),
            _csrw(csr, value_reg),
            _csrr(value_reg, csr),
            write_sigupd(value_reg, test_data),
        ])
    for csr in VS_H_ACCESS_CSRS:
        lines.extend([
            "",
            test_data.add_testcase(f"m_{csr[0]}", "cp_replica", "H_mcsr_cg"),
            _csrw(csr[0], value_reg),
            _csrr(value_reg, csr[0]),
            write_sigupd(value_reg, test_data),
        ])

    lines.extend([
        "",
        comment_banner("cp_mtvala", "mtval must not be read-only zero"),
        _csrr(value_reg, "mtval"),
        f"LI(x{value_reg}, -1)",
        test_data.add_testcase("write_ones", "cp_mtvala", "H_mcsr_cg"),
        gen_csr_write_sigupd(value_reg, "mtval", test_data),
    ])
    _csrw("mtval", value_reg)

    lines.append(comment_banner("cp_hcsr_access", "HS-mode access to HS and VS H-extension CSRs"))
    for csr in HS_H_ACCESS_CSRS + VS_H_ACCESS_CSRS:
        lines.extend(csr_access_test(test_data, csr, "H_hscsr_cg", "cp_hcsr_access"))

    lines.append(comment_banner("cp_hcsrwalk", "HS-mode walk of HS and VS H-extension CSRs"))
    for csr in HS_H_ACCESS_CSRS + VS_H_ACCESS_CSRS:
        if csr[0] == "hstatus" or csr[0] == "vsstatus":
            continue
        lines.extend(csr_walk_test(test_data, csr, "H_hscsr_cg", "cp_hcsrwalk"))

    lines.append(comment_banner("cp_replica", "HS-mode replica write/read"))
    lines.append(f"LI(x{value_reg}, 0x2468)")
    for csr in S_REPLICA_CSRS:
        lines.extend([
            "",
            test_data.add_testcase(f"hs_{csr}", "cp_replica", "H_hscsr_cg"),
            _csrw(csr, value_reg),
            _csrr(value_reg, csr),
            write_sigupd(value_reg, test_data),
        ])
    for csr in VS_H_ACCESS_CSRS:
        lines.extend([
            "",
            test_data.add_testcase(f"hs_{csr[0]}", "cp_replica", "H_hscsr_cg"),
            _csrw(csr[0], value_reg),
            _csrr(value_reg, csr[0]),
            write_sigupd(value_reg, test_data),
        ])

    lines.extend([
        "",
        comment_banner("cp_hstatus_vgein", "Write representative hstatus.VGEIN values"),
        _csrr(scratch, "hstatus"),
    ])
    for value in (0, 1, 2, 63):
        lines.extend([
            "",
            f"LI(x{value_reg}, {value << 12})",
            f"LI(x{scratch}, 0x3f000)",
            f"not x{scratch}, x{scratch}",
            f"and x{value_reg}, x{value_reg}, x{scratch}",
            f"or x{value_reg}, x{value_reg}, x{scratch}",
            test_data.add_testcase(f"vgein_{value}", "cp_hstatus_vgein", "H_hscsr_cg"),
            gen_csr_write_sigupd(value_reg, "hstatus", test_data),
        ])
    _csrw("hstatus", scratch)

    lines.append(comment_banner("cp_vscause_write", "Write WLRL vscause interrupt and exception encodings"))
    for interrupt in (0, 1):
        for cause in (0, 1, 2, 15, 22, 63):
            lines.extend([
                "",
                f"LI(x{value_reg}, {cause})",
                f"LI(x{scratch}, {interrupt << (63 if interrupt else 0)})" if interrupt else f"LI(x{scratch}, 0)",
                f"or x{value_reg}, x{value_reg}, x{scratch}",
                test_data.add_testcase(f"i{interrupt}_cause{cause}", "cp_vscause_write", "H_hscsr_cg"),
                gen_csr_write_sigupd(value_reg, "vscause", test_data),
            ])

    lines.extend([
        "",
        comment_banner("cp_tvm", "TVM/VTVM trap behavior for satp and hgatp"),
        _csrr(value_reg, "mstatus"),
        _csrr(scratch, "hstatus"),
    ])
    for tvm in (0, 1):
        for vtvm in (0, 1):
            for csr in ("satp", "hgatp"):
                lines.extend([
                    "",
                    f"LI(x{value_reg}, {tvm << 20})",
                    _csrs("mstatus", value_reg) if tvm else _csrc("mstatus", value_reg),
                    f"LI(x{value_reg}, {vtvm << 20})",
                    _csrs("hstatus", value_reg) if vtvm else _csrc("hstatus", value_reg),
                    test_data.add_testcase(f"{csr}_tvm{tvm}_vtvm{vtvm}", "cp_tvm", "H_hscsr_cg"),
                    _csrr(value_reg, csr),
                    write_sigupd(value_reg, test_data),
                ])
    _csrw("mstatus", value_reg)
    _csrw("hstatus", scratch)
    test_data.int_regs.return_registers([value_reg, scratch])

    lines.append(comment_banner("cp_hcsr_virtualinstructionfault", "HS and VS CSR direct accesses trap virtually in VS-mode"))
    for csr in HS_H_ACCESS_CSRS + VS_H_ACCESS_CSRS:
        lines.extend([
            "",
            test_data.add_testcase(f"vs_{csr[0]}", "cp_hcsr_virtualinstructionfault", "H_vscsr_cg"),
            _csrr(value_reg, csr[0]),
            "nop",
        ])

    lines.append(comment_banner("cp_hcsr_inaccessible", "Machine H-extension CSRs are inaccessible"))
    for mode, covergroup in (("VS", "H_vscsr_cg"), ("U", "H_ucsr_cg"), ("VU", "H_vucsr_cg")):
        for csr in ("mtval2", "mtinst"):
            lines.extend([
                "",
                _goto_mode(mode),
                test_data.add_testcase(f"{mode.lower()}_{csr}", "cp_hcsr_inaccessible", covergroup),
                _csrr(value_reg, csr),
                "nop",
            ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_illegalupper", "High-half H CSRs are illegal when XLEN > 32"))
    if True:
        for mode, covergroup in (("VS", "H_vscsr_cg"), ("U", "H_ucsr_cg"), ("VU", "H_vucsr_cg")):
            for csr in HIGH_HALF_CSRS:
                lines.extend([
                    "#if __riscv_xlen == 64",
                    _goto_mode(mode),
                    test_data.add_testcase(f"{mode.lower()}_{csr}", "cp_illegalupper", covergroup),
                    _csrr(value_reg, csr),
                    "nop",
                    "#endif",
                ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_nonreplica", "Nonreplicated supervisor CSRs remain accessible in VS-mode"))
    lines.append(_goto_mode("VS"))
    for csr in S_NONREPLICA_CSRS:
        lines.extend([
            "",
            test_data.add_testcase(csr, "cp_nonreplica", "H_vscsr_cg"),
            _csrr(value_reg, csr),
            write_sigupd(value_reg, test_data),
        ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_replica", "VS-mode uses VS replicas for supervisor CSR accesses"))
    lines.append(_goto_mode("VS"))
    for csr in S_REPLICA_CSRS + [c[0] for c in VS_H_ACCESS_CSRS]:
        lines.extend([
            "",
            test_data.add_testcase(f"vs_{csr}", "cp_replica", "H_vscsr_cg"),
            _csrw(csr, value_reg),
            _csrr(value_reg, csr),
            write_sigupd(value_reg, test_data),
        ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_vsstatus_sd_write", "vsstatus SD depends on FS and VS"))
    for fs in range(4):
        for vs_bits in range(4):
            fields = (fs << 13) | (vs_bits << 9)
            lines.extend([
                "",
                _goto_mode("VS"),
                f"LI(x{value_reg}, 0x{fields:x})",
                test_data.add_testcase(f"fs{fs}_vs{vs_bits}", "cp_vsstatus_sd_write", "H_vscsr_cg"),
                gen_csr_write_sigupd(value_reg, "vsstatus", test_data),
                _goto_mode("M"),
            ])

    lines.append(comment_banner("cp_tvm", "VTVM traps satp in VS-mode"))
    for vtvm in (0, 1):
        lines.extend([
            "",
            f"LI(x{value_reg}, {vtvm << 20})",
            _csrs("hstatus", value_reg) if vtvm else _csrc("hstatus", value_reg),
            _goto_mode("VS"),
            test_data.add_testcase(f"satp_vtvm{vtvm}", "cp_tvm", "H_vscsr_cg"),
            _csrr(value_reg, "satp"),
            write_sigupd(value_reg, test_data),
            _goto_mode("M"),
        ])

    lines.append(comment_banner("cp_hcsr_inaccessible", "H-extension CSRs are inaccessible below M-mode"))
    for mode, covergroup, inaccessible_csrs in (
        ("U", "H_ucsr_cg", [c[0] for c in HS_H_ACCESS_CSRS]),
        ("VU", "H_vucsr_cg", [c[0] for c in HS_H_ACCESS_CSRS + VS_H_ACCESS_CSRS]),
    ):
        lines.append(_goto_mode(mode))
        for csr in inaccessible_csrs:
            lines.extend([
                "",
                test_data.add_testcase(f"{mode.lower()}_{csr}", "cp_hcsr_inaccessible", covergroup),
                _csrr(value_reg, csr),
                "nop",
            ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_scsr", "Supervisor CSR access faults in U and VU modes"))
    for mode, covergroup, csr_names in (
        ("U", "H_ucsr_cg", S_REPLICA_CSRS + S_NONREPLICA_CSRS),
        ("VU", "H_vucsr_cg", S_REPLICA_CSRS + S_NONREPLICA_CSRS + [c[0] for c in VS_H_ACCESS_CSRS]),
    ):
        lines.append(_goto_mode(mode))
        for csr in csr_names:
            lines.extend([
                "",
                test_data.add_testcase(f"{mode.lower()}_{csr}", "cp_scsr", covergroup),
                _csrr(value_reg, csr),
                "nop",
            ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_hlv", "Execute HLV instructions"))
    lines.append(f"LA(x{scratch}, scratch)")
    for mode in ("M", "S", "U"):
        lines.append(_goto_mode(mode))
        if mode == "U":
            lines.extend([f"LI(x{value_reg}, 0x200)", _csrs("hstatus", value_reg)])
        for instr in ("hlv.b", "hlv.bu", "hlv.h", "hlv.hu", "hlv.w"):
            lines.extend([
                "",
                test_data.add_testcase(f"{mode.lower()}_{instr.replace('.', '_')}", "cp_hlv", "H_inst_cg"),
                f"{instr} x{value_reg}, 0(x{scratch})",
                "nop",
                write_sigupd(value_reg, test_data),
            ])
        if test_data.xlen == 64:
            for instr in ("hlv.wu", "hlv.d"):
                lines.extend([
                    "",
                    test_data.add_testcase(f"{mode.lower()}_{instr.replace('.', '_')}", "cp_hlv", "H_inst_cg"),
                    f"{instr} x{value_reg}, 0(x{scratch})",
                    "nop",
                    write_sigupd(value_reg, test_data),
                ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_hlvx", "Execute HLVX instructions"))
    for mode in ("M", "S", "U"):
        lines.append(_goto_mode(mode))
        for instr in ("hlvx.hu", "hlvx.wu"):
            lines.extend([
                "",
                test_data.add_testcase(f"{mode.lower()}_{instr.replace('.', '_')}", "cp_hlvx", "H_inst_cg"),
                f"{instr} x{value_reg}, 0(x{scratch})",
                "nop",
                write_sigupd(value_reg, test_data),
            ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_hsv", "Execute HSV instructions"))
    for mode in ("M", "S", "U"):
        lines.append(_goto_mode(mode))
        for instr in ("hsv.b", "hsv.h", "hsv.w"):
            lines.extend([
                f"LI(x{value_reg}, 0x12345678)",
                "",
                test_data.add_testcase(f"{mode.lower()}_{instr.replace('.', '_')}", "cp_hsv", "H_inst_cg"),
                f"{instr} x{value_reg}, 0(x{scratch})",
                "nop",
                write_sigupd(value_reg, test_data),
            ])
        if test_data.xlen == 64:
            lines.extend([
                f"LI(x{value_reg}, 0x123456789abcdef0)",
                test_data.add_testcase(f"{mode.lower()}_hsv_d", "cp_hsv", "H_inst_cg"),
                "hsv.d x{} , 0(x{})".format(value_reg, scratch),
                "nop",
                write_sigupd(value_reg, test_data),
            ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_hfence", "Execute HFENCE instructions"))
    reg, save_status, save_hstatus = test_data.int_regs.get_registers(3)
    lines.extend([_csrr(save_status, "mstatus"), _csrr(save_hstatus, "hstatus")])
    for mode in ("M", "S"):
        for tvm in (0, 1):
            for vtvm in (0, 1):
                lines.extend([
                    f"LI(x{reg}, {tvm << 20})",
                    _csrs("mstatus", reg) if tvm else _csrc("mstatus", reg),
                    f"LI(x{reg}, {vtvm << 20})",
                    _csrs("hstatus", reg) if vtvm else _csrc("hstatus", reg),
                    _goto_mode(mode),
                    test_data.add_testcase(f"{mode.lower()}_vvma_tvm{tvm}_vtvm{vtvm}", "cp_hfence", "H_inst_cg"),
                    "hfence.vvma",
                    "nop",
                    test_data.add_testcase(f"{mode.lower()}_gvma_tvm{tvm}_vtvm{vtvm}", "cp_hfence", "H_inst_cg"),
                    "hfence.gvma",
                    "nop",
                ])
    lines.append(_goto_mode("M"))

    lines.append(comment_banner("cp_sfence", "Execute SFENCE and SINVAL instructions"))
    for mode in ("M", "S", "VS"):
        for tvm in (0, 1):
            for vtvm in (0, 1):
                lines.extend([
                    f"LI(x{reg}, {tvm << 20})",
                    _csrs("mstatus", reg) if tvm else _csrc("mstatus", reg),
                    f"LI(x{reg}, {vtvm << 20})",
                    _csrs("hstatus", reg) if vtvm else _csrc("hstatus", reg),
                    _goto_mode(mode),
                    test_data.add_testcase(f"{mode.lower()}_sfence_tvm{tvm}_vtvm{vtvm}", "cp_sfence", "H_inst_cg"),
                    "sfence.vma",
                    "nop",
                    _goto_mode("M"),
                ])
    lines.extend([_csrw("mstatus", save_status), _csrw("hstatus", save_hstatus)])
    test_data.int_regs.return_registers([reg, save_status, save_hstatus])

    lines.append(comment_banner("cp_mret_m", "Execute mret in M-mode"))
    reg, retaddr, save_status, save_hstatus = test_data.int_regs.get_registers(4)
    lines.extend([_csrr(save_status, "mstatus"), _csrr(save_hstatus, "hstatus")])
    for mpp in (0, 1, 3):
        for mpv in (0, 1):
            for mpie in (0, 1):
                lines.extend([
                    f"LA(x{retaddr}, 1f)",
                    _csrw("mepc", retaddr),
                    f"LI(x{reg}, {(mpp << 11) | (mpv << 39 if test_data.xlen == 64 else 0) | (mpie << 7)})",
                    _csrs("mstatus", reg),
                    test_data.add_testcase(f"mpp{mpp}_mpv{mpv}_mpie{mpie}", "cp_mret_m", "H_inst_cg"),
                    "mret",
                    "nop",
                    "1:",
                    write_sigupd(reg, test_data),
                    _goto_mode("M"),
                ])

    lines.append(comment_banner("cp_mret_illegal", "Execute mret below M-mode"))
    for mode in ("S", "VS", "U", "VU"):
        lines.extend([
            _goto_mode(mode),
            test_data.add_testcase(mode.lower(), "cp_mret_illegal", "H_inst_cg"),
            "mret",
            "nop",
            _goto_mode("M"),
        ])

    lines.append(comment_banner("cp_sret_illegal", "Execute sret in VU-mode"))
    lines.extend([_goto_mode("VU"), test_data.add_testcase("vu", "cp_sret_illegal", "H_inst_cg"), "sret", "nop", _goto_mode("M")])

    lines.append(comment_banner("cp_sret_m", "Execute sret in M-mode"))
    for spp in (0, 1):
        for spv in (0, 1):
            for spie in (0, 1):
                lines.extend([
                    f"LA(x{retaddr}, 2f)",
                    _csrw("sepc", retaddr),
                    f"LI(x{reg}, {(spp << 8) | (spie << 5)})",
                    _csrs("sstatus", reg),
                    f"LI(x{reg}, {spv << 7})",
                    _csrs("hstatus", reg),
                    test_data.add_testcase(f"spp{spp}_spv{spv}_spie{spie}", "cp_sret_m", "H_inst_cg"),
                    "sret",
                    "nop",
                    "2:",
                    write_sigupd(reg, test_data),
                    _goto_mode("M"),
                ])

    lines.append(comment_banner("cp_sret_hs", "Execute sret in HS-mode"))
    for spp in (0, 1):
        for spv in (0, 1):
            for spie in (0, 1):
                lines.extend([
                    _goto_mode("S"),
                    f"LA(x{retaddr}, 3f)",
                    _csrw("sepc", retaddr),
                    f"LI(x{reg}, {(spp << 8) | (spie << 5)})",
                    _csrs("sstatus", reg),
                    f"LI(x{reg}, {spv << 7})",
                    _csrs("hstatus", reg),
                    test_data.add_testcase(f"spp{spp}_spv{spv}_spie{spie}", "cp_sret_hs", "H_inst_cg"),
                    "sret",
                    "nop",
                    "3:",
                    write_sigupd(reg, test_data),
                    _goto_mode("M"),
                ])

    lines.append(comment_banner("cp_sret_vs", "Execute sret in VS-mode"))
    for spp in (0, 1):
        for spie in (0, 1):
            for vtsr in (0, 1):
                lines.extend([
                    f"LI(x{reg}, {vtsr << 22})",
                    _csrs("hstatus", reg) if vtsr else _csrc("hstatus", reg),
                    _goto_mode("VS"),
                    f"LA(x{retaddr}, 4f)",
                    _csrw("vsepc", retaddr),
                    f"LI(x{reg}, {(spp << 8) | (spie << 5)})",
                    _csrs("vsstatus", reg),
                    test_data.add_testcase(f"spp{spp}_spie{spie}_vtsr{vtsr}", "cp_sret_vs", "H_inst_cg"),
                    "sret",
                    "nop",
                    "4:",
                    write_sigupd(reg, test_data),
                    _goto_mode("M"),
                ])

    lines.extend([_csrw("mstatus", save_status), _csrw("hstatus", save_hstatus)])
    test_data.int_regs.return_registers([reg, retaddr, save_status, save_hstatus])

    return lines


@add_priv_test_generator(
    "H",
    extra_defines=["#define RVTEST_ENABLE_H", "#define RVTEST_HYPERVISOR"],
    required_extensions=["H", "Zicsr"],
    march_extensions=["H", "Zicsr"],
)
def make_h(test_data: TestData) -> list[TestChunk]:
    """Generate tests for the H hypervisor suite for the workspace output tree."""
    test_chunks: list[TestChunk] = []

    tc = test_data.begin_test_chunk("workspace_h")
    tc.code.extend(_generate_workspace_h_csr_tests(test_data))
    test_chunks.append(test_data.end_test_chunk())

    return test_chunks
