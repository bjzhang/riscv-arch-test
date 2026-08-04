///////////////////////////////////////////
//
// RISC-V Architectural Functional Coverage Covergroups
//
// Written: Codex assistant 30 July 2026
//
// SPDX-License-Identifier: Apache-2.0
//
////////////////////////////////////////////////////////////////////////////////////////////////

`define COVER_H

covergroup H_mcsr_cg with function sample(ins_t ins);
    option.per_instance = 0;
    `include "general/RISCV_coverage_standard_coverpoints.svh"

    hcsr_op: coverpoint ins.current.insn {
        wildcard bins csrrw = {CSRRW};
        wildcard bins csrrs = {CSRRS};
        wildcard bins csrrc = {CSRRC};
        wildcard bins csrr = {CSRR};
    }

    hcsr_name: coverpoint ins.current.insn[31:20] {
        bins mtval2 = {CSR_MTVAL2};
        bins mtinst = {CSR_MTINST};
        bins hstatus = {CSR_HSTATUS};
        bins hedeleg = {CSR_HEDELEG};
        bins hideleg = {CSR_HIDELEG};
        bins hie = {CSR_HIE};
        bins htimedelta = {CSR_HTIMEDELTA};
        bins hcounteren = {CSR_HCOUNTEREN};
        bins hgeie = {CSR_HGEIE};
        bins henvcfg = {CSR_HENVCFG};
        bins htval = {CSR_HTVAL};
        bins hip = {CSR_HIP};
        bins hvip = {CSR_HVIP};
        bins htinst = {CSR_HTINST};
        bins hgatp = {CSR_HGATP};
        bins hgeip = {CSR_HGEIP};
    `ifdef UDB_MXLEN_32
        bins hedelegh = {CSR_HEDELEGH};
        bins htimedeltah = {CSR_HTIMEDELTAH};
        bins henvcfgh = {CSR_HENVCFGH};
    `endif
    }

    replica_name: coverpoint ins.current.insn[31:20] {
        bins sstatus = {CSR_SSTATUS};
        bins sie = {CSR_SIE};
        bins stvec = {CSR_STVEC};
        bins sscratch = {CSR_SSCRATCH};
        bins sepc = {CSR_SEPC};
        bins scause = {CSR_SCAUSE};
        bins stval = {CSR_STVAL};
        bins sip = {CSR_SIP};
        bins satp = {CSR_SATP};
        bins vsstatus = {CSR_VSSTATUS};
        bins vsie = {CSR_VSIE};
        bins vstvec = {CSR_VSTVEC};
        bins vsscratch = {CSR_VSSCRATCH};
        bins vsepc = {CSR_VSEPC};
        bins vscause = {CSR_VSCAUSE};
        bins vstval = {CSR_VSTVAL};
        bins vsip = {CSR_VSIP};
        bins vsatp = {CSR_VSATP};
    }

    write_pattern: coverpoint ins.current.rs1_val {
        bins all_zeros = {'0};
        bins all_ones = {'1};
        bins other = default;
    }

    bitwalk_kind: coverpoint $countones(ins.current.rs1_val) {
        bins none = {0};
        bins one = {1};
        bins many = default;
    }

    mtval_name: coverpoint ins.current.insn[31:20] {
        bins mtval = {CSR_MTVAL};
    }

    cp_hcsr_access: cross priv_mode_m, hcsr_op, hcsr_name, write_pattern;
    cp_hcsrwalk: cross priv_mode_m, hcsr_op, hcsr_name, bitwalk_kind;
    cp_replica: cross priv_mode_m, hcsr_op, replica_name, write_pattern;
    cp_mtvala: cross priv_mode_m, hcsr_op, mtval_name, write_pattern;

endgroup

covergroup H_hscsr_cg with function sample(ins_t ins);
    option.per_instance = 0;
    `include "general/RISCV_coverage_standard_coverpoints.svh"

    hcsr_op: coverpoint ins.current.insn {
        wildcard bins csrrw = {CSRRW};
        wildcard bins csrrs = {CSRRS};
        wildcard bins csrrc = {CSRRC};
        wildcard bins csrr = {CSRR};
    }

    hs_name: coverpoint ins.current.insn[31:20] {
        bins hstatus = {CSR_HSTATUS};
        bins hedeleg = {CSR_HEDELEG};
        bins hideleg = {CSR_HIDELEG};
        bins hie = {CSR_HIE};
        bins htimedelta = {CSR_HTIMEDELTA};
        bins hcounteren = {CSR_HCOUNTEREN};
        bins hgeie = {CSR_HGEIE};
        bins henvcfg = {CSR_HENVCFG};
        bins htval = {CSR_HTVAL};
        bins hip = {CSR_HIP};
        bins hvip = {CSR_HVIP};
        bins htinst = {CSR_HTINST};
        bins hgatp = {CSR_HGATP};
        bins hgeip = {CSR_HGEIP};
    `ifdef UDB_MXLEN_32
        bins hedelegh = {CSR_HEDELEGH};
        bins htimedeltah = {CSR_HTIMEDELTAH};
        bins henvcfgh = {CSR_HENVCFGH};
    `endif
        bins vsstatus = {CSR_VSSTATUS};
        bins vsie = {CSR_VSIE};
        bins vstvec = {CSR_VSTVEC};
        bins vsscratch = {CSR_VSSCRATCH};
        bins vsepc = {CSR_VSEPC};
        bins vscause = {CSR_VSCAUSE};
        bins vstval = {CSR_VSTVAL};
        bins vsip = {CSR_VSIP};
        bins vsatp = {CSR_VSATP};
    }

    hs_walk_name: coverpoint ins.current.insn[31:20] {
        bins hedeleg = {CSR_HEDELEG};
        bins hideleg = {CSR_HIDELEG};
        bins hie = {CSR_HIE};
        bins htimedelta = {CSR_HTIMEDELTA};
        bins hcounteren = {CSR_HCOUNTEREN};
        bins hgeie = {CSR_HGEIE};
        bins henvcfg = {CSR_HENVCFG};
        bins htval = {CSR_HTVAL};
        bins hip = {CSR_HIP};
        bins hvip = {CSR_HVIP};
        bins htinst = {CSR_HTINST};
        bins hgatp = {CSR_HGATP};
        bins hgeip = {CSR_HGEIP};
    `ifdef UDB_MXLEN_32
        bins hedelegh = {CSR_HEDELEGH};
        bins htimedeltah = {CSR_HTIMEDELTAH};
        bins henvcfgh = {CSR_HENVCFGH};
    `endif
        bins vsie = {CSR_VSIE};
        bins vsip = {CSR_VSIP};
        bins vstval = {CSR_VSTVAL};
        bins vstvec = {CSR_VSTVEC};
        bins vsscratch = {CSR_VSSCRATCH};
        bins vsepc = {CSR_VSEPC};
        bins vscause = {CSR_VSCAUSE};
        bins vsatp = {CSR_VSATP};
    }

    machine_hcsr_name: coverpoint ins.current.insn[31:20] {
        bins mtval2 = {CSR_MTVAL2};
        bins mtinst = {CSR_MTINST};
    }

    replica_name: coverpoint ins.current.insn[31:20] {
        bins sstatus = {CSR_SSTATUS};
        bins sie = {CSR_SIE};
        bins stvec = {CSR_STVEC};
        bins sscratch = {CSR_SSCRATCH};
        bins sepc = {CSR_SEPC};
        bins scause = {CSR_SCAUSE};
        bins stval = {CSR_STVAL};
        bins sip = {CSR_SIP};
        bins satp = {CSR_SATP};
        bins vsstatus = {CSR_VSSTATUS};
        bins vsie = {CSR_VSIE};
        bins vstvec = {CSR_VSTVEC};
        bins vsscratch = {CSR_VSSCRATCH};
        bins vsepc = {CSR_VSEPC};
        bins vscause = {CSR_VSCAUSE};
        bins vstval = {CSR_VSTVAL};
        bins vsip = {CSR_VSIP};
        bins vsatp = {CSR_VSATP};
    }

    write_pattern: coverpoint ins.current.rs1_val {
        bins all_zeros = {'0};
        bins all_ones = {'1};
        bins other = default;
    }

    bitwalk_kind: coverpoint $countones(ins.current.rs1_val) {
        bins none = {0};
        bins one = {1};
        bins many = default;
    }

    hstatus_vgein: coverpoint ins.current.rs1_val {
        bins zero = {'0};
        bins one = {1};
        bins edge = {63};
        bins other = default;
    }

    vscause_int: coverpoint ins.current.rs1_val[`UDB_MXLEN-1] {
        bins clear = {0};
        bins set = {1};
    }

    vscause_code: coverpoint ins.current.rs1_val[`UDB_MXLEN-2:0] {
        bins exception = {[0:15]};
        bins interrupt = {[16:64]};
    }

    mstatus_tvm: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "mstatus", "tvm")[0] {
        bins disabled = {0};
        bins enabled = {1};
    }

    hstatus_vtvm: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "hstatus", "vtvm")[0] {
        bins disabled = {0};
        bins enabled = {1};
    }

    satp_name: coverpoint ins.current.insn[31:20] {
        bins satp = {CSR_SATP};
        bins hgatp = {CSR_HGATP};
    }

    cp_hcsr_access: cross priv_mode_hs, hcsr_op, hs_name, write_pattern;
    cp_hcsrwalk: cross priv_mode_hs, hcsr_op, hs_walk_name, bitwalk_kind;
    cp_hcsr_inaccessible: cross priv_mode_hs, hcsr_op, machine_hcsr_name;
    cp_replica: cross priv_mode_hs, hcsr_op, replica_name, write_pattern;
    cp_hstatus_vgein: cross priv_mode_hs, hcsr_op, hstatus_vgein;
    cp_vscause_write: cross priv_mode_hs, hcsr_op, vscause_int, vscause_code;
    cp_tvm: cross priv_mode_hs, mstatus_tvm, satp_name, hcsr_op;

endgroup

covergroup H_vscsr_cg with function sample(ins_t ins);
    option.per_instance = 0;
    `include "general/RISCV_coverage_standard_coverpoints.svh"

    csr_op: coverpoint ins.current.insn {
        wildcard bins csrrw = {CSRRW};
        wildcard bins csrrs = {CSRRS};
        wildcard bins csrrc = {CSRRC};
        wildcard bins csrr = {CSRR};
    }

    machine_hcsr_name: coverpoint ins.current.insn[31:20] {
        bins mtval2 = {CSR_MTVAL2};
        bins mtinst = {CSR_MTINST};
    }

    hcsr_name: coverpoint ins.current.insn[31:20] {
        bins hstatus = {CSR_HSTATUS};
        bins hedeleg = {CSR_HEDELEG};
        bins hideleg = {CSR_HIDELEG};
        bins hie = {CSR_HIE};
        bins htimedelta = {CSR_HTIMEDELTA};
        bins hcounteren = {CSR_HCOUNTEREN};
        bins hgeie = {CSR_HGEIE};
        bins henvcfg = {CSR_HENVCFG};
        bins htval = {CSR_HTVAL};
        bins hip = {CSR_HIP};
        bins hvip = {CSR_HVIP};
        bins htinst = {CSR_HTINST};
        bins hgatp = {CSR_HGATP};
        bins hgeip = {CSR_HGEIP};
    `ifdef UDB_MXLEN_32
        bins hedelegh = {CSR_HEDELEGH};
        bins htimedeltah = {CSR_HTIMEDELTAH};
        bins henvcfgh = {CSR_HENVCFGH};
        bins vstimecmph = {CSR_VSTIMECMPH};
    `endif
        bins vsstatus = {CSR_VSSTATUS};
        bins vsie = {CSR_VSIE};
        bins vstvec = {CSR_VSTVEC};
        bins vsscratch = {CSR_VSSCRATCH};
        bins vsepc = {CSR_VSEPC};
        bins vscause = {CSR_VSCAUSE};
        bins vstval = {CSR_VSTVAL};
        bins vsip = {CSR_VSIP};
        bins vsatp = {CSR_VSATP};
    }

    hhalf_name: coverpoint ins.current.insn[31:20] {
    `ifdef UDB_MXLEN_64
        bins hedelegh = {CSR_HEDELEGH};
        bins htimedeltah = {CSR_HTIMEDELTAH};
        bins henvcfgh = {CSR_HENVCFGH};
        bins vstimecmph = {CSR_VSTIMECMPH};
    `else
        bins rv32_only = {CSR_HEDELEGH};
    `endif
    }

    replica_name: coverpoint ins.current.insn[31:20] {
        bins sstatus = {CSR_SSTATUS};
        bins sie = {CSR_SIE};
        bins stvec = {CSR_STVEC};
        bins sscratch = {CSR_SSCRATCH};
        bins sepc = {CSR_SEPC};
        bins scause = {CSR_SCAUSE};
        bins stval = {CSR_STVAL};
        bins sip = {CSR_SIP};
        bins satp = {CSR_SATP};
        bins vsstatus = {CSR_VSSTATUS};
        bins vsie = {CSR_VSIE};
        bins vstvec = {CSR_VSTVEC};
        bins vsscratch = {CSR_VSSCRATCH};
        bins vsepc = {CSR_VSEPC};
        bins vscause = {CSR_VSCAUSE};
        bins vstval = {CSR_VSTVAL};
        bins vsip = {CSR_VSIP};
        bins vsatp = {CSR_VSATP};
    }

    nonreplica_name: coverpoint ins.current.insn[31:20] {
        bins scounteren = {CSR_SCOUNTEREN};
        bins senvcfg = {CSR_SENVCFG};
        bins scountinhibit = {CSR_SCOUNTINHIBIT};
    }

    write_pattern: coverpoint ins.current.rs1_val {
        bins all_zeros = {'0};
        bins all_ones = {'1};
        bins other = default;
    }

    satp_name: coverpoint ins.current.insn[31:20] {
        bins satp = {CSR_SATP};
    }

    vsstatus_sd: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "vsstatus", "sd")[0] {
        bins clear = {0};
        bins set = {1};
    }

    vsstatus_fs: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "vsstatus", "fs") {
        bins zero = {0};
        bins nonzero = {[1:3]};
    }

    vsstatus_vs: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "vsstatus", "vs") {
        bins zero = {0};
        bins nonzero = {[1:3]};
    }

    hstatus_vtvm: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "hstatus", "vtvm")[0] {
        bins disabled = {0};
        bins enabled = {1};
    }

    mstatus_tvm: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "mstatus", "tvm")[0] {
        bins disabled = {0};
        bins enabled = {1};
    }

    cp_hcsr_inaccessible: cross priv_mode_vs, csr_op, machine_hcsr_name;
    cp_hcsr_virtualinstructionfault: cross priv_mode_vs, csr_op, hcsr_name;
    `ifdef UDB_MXLEN_64
        cp_illegalupper: cross priv_mode_vs, csr_op, hhalf_name;
    `endif
    cp_replica: cross priv_mode_vs, csr_op, replica_name, write_pattern;
    cp_nonreplica: cross priv_mode_vs, csr_op, nonreplica_name, write_pattern;
    cp_vsstatus_sd_write: cross priv_mode_vs, vsstatus_sd, vsstatus_fs, vsstatus_vs;
    cp_tvm: cross priv_mode_vs, hstatus_vtvm, satp_name, csr_op;

endgroup

covergroup H_ucsr_cg with function sample(ins_t ins);
    option.per_instance = 0;
    `include "general/RISCV_coverage_standard_coverpoints.svh"

    csr_op: coverpoint ins.current.insn {
        wildcard bins csrrw = {CSRRW};
        wildcard bins csrrs = {CSRRS};
        wildcard bins csrrc = {CSRRC};
        wildcard bins csrr = {CSRR};
    }

    hcsr_name: coverpoint ins.current.insn[31:20] {
        bins mtval2 = {CSR_MTVAL2};
        bins mtinst = {CSR_MTINST};
        bins hstatus = {CSR_HSTATUS};
        bins hedeleg = {CSR_HEDELEG};
        bins hideleg = {CSR_HIDELEG};
        bins hie = {CSR_HIE};
        bins hcounteren = {CSR_HCOUNTEREN};
        bins hgeie = {CSR_HGEIE};
        bins henvcfg = {CSR_HENVCFG};
        bins htval = {CSR_HTVAL};
        bins hip = {CSR_HIP};
        bins hvip = {CSR_HVIP};
        bins htinst = {CSR_HTINST};
        bins hgatp = {CSR_HGATP};
        bins hgeip = {CSR_HGEIP};
    }

    hhalf_name: coverpoint ins.current.insn[31:20] {
    `ifdef UDB_MXLEN_64
        bins hedelegh = {CSR_HEDELEGH};
        bins htimedeltah = {CSR_HTIMEDELTAH};
        bins henvcfgh = {CSR_HENVCFGH};
        bins vstimecmph = {CSR_VSTIMECMPH};
    `else
        bins rv32_only = {CSR_HEDELEGH};
    `endif
    }

    scsr_name: coverpoint ins.current.insn[31:20] {
        bins sstatus = {CSR_SSTATUS};
        bins sie = {CSR_SIE};
        bins stvec = {CSR_STVEC};
        bins sscratch = {CSR_SSCRATCH};
        bins sepc = {CSR_SEPC};
        bins scause = {CSR_SCAUSE};
        bins stval = {CSR_STVAL};
        bins sip = {CSR_SIP};
        bins satp = {CSR_SATP};
        bins scounteren = {CSR_SCOUNTEREN};
        bins senvcfg = {CSR_SENVCFG};
        bins scountinhibit = {CSR_SCOUNTINHIBIT};
    }

    write_pattern: coverpoint ins.current.rs1_val {
        bins all_zeros = {'0};
        bins all_ones = {'1};
        bins other = default;
    }

    cp_hcsr_inaccessible: cross priv_mode_u, csr_op, hcsr_name;
    `ifdef UDB_MXLEN_64
        cp_illegalupper: cross priv_mode_u, csr_op, hhalf_name;
    `endif
    cp_scsr: cross priv_mode_u, csr_op, scsr_name, write_pattern;

endgroup

covergroup H_vucsr_cg with function sample(ins_t ins);
    option.per_instance = 0;
    `include "general/RISCV_coverage_standard_coverpoints.svh"

    csr_op: coverpoint ins.current.insn {
        wildcard bins csrrw = {CSRRW};
        wildcard bins csrrs = {CSRRS};
        wildcard bins csrrc = {CSRRC};
        wildcard bins csrr = {CSRR};
    }

    hcsr_name: coverpoint ins.current.insn[31:20] {
        bins mtval2 = {CSR_MTVAL2};
        bins mtinst = {CSR_MTINST};
        bins hstatus = {CSR_HSTATUS};
        bins hedeleg = {CSR_HEDELEG};
        bins hideleg = {CSR_HIDELEG};
        bins hie = {CSR_HIE};
        bins hcounteren = {CSR_HCOUNTEREN};
        bins hgeie = {CSR_HGEIE};
        bins henvcfg = {CSR_HENVCFG};
        bins htval = {CSR_HTVAL};
        bins hip = {CSR_HIP};
        bins hvip = {CSR_HVIP};
        bins htinst = {CSR_HTINST};
        bins hgatp = {CSR_HGATP};
        bins hgeip = {CSR_HGEIP};
    `ifdef UDB_MXLEN_32
        bins hedelegh = {CSR_HEDELEGH};
        bins htimedeltah = {CSR_HTIMEDELTAH};
        bins henvcfgh = {CSR_HENVCFGH};
        bins vstimecmph = {CSR_VSTIMECMPH};
    `endif
        bins vsstatus = {CSR_VSSTATUS};
        bins vsie = {CSR_VSIE};
        bins vstvec = {CSR_VSTVEC};
        bins vsscratch = {CSR_VSSCRATCH};
        bins vsepc = {CSR_VSEPC};
        bins vscause = {CSR_VSCAUSE};
        bins vstval = {CSR_VSTVAL};
        bins vsip = {CSR_VSIP};
        bins vsatp = {CSR_VSATP};
        bins sstatus = {CSR_SSTATUS};
        bins sie = {CSR_SIE};
        bins stvec = {CSR_STVEC};
        bins sscratch = {CSR_SSCRATCH};
        bins sepc = {CSR_SEPC};
        bins scause = {CSR_SCAUSE};
        bins stval = {CSR_STVAL};
        bins sip = {CSR_SIP};
        bins satp = {CSR_SATP};
    }

    hhalf_name: coverpoint ins.current.insn[31:20] {
    `ifdef UDB_MXLEN_64
        bins hedelegh = {CSR_HEDELEGH};
        bins htimedeltah = {CSR_HTIMEDELTAH};
        bins henvcfgh = {CSR_HENVCFGH};
        bins vstimecmph = {CSR_VSTIMECMPH};
    `else
        bins rv32_only = {CSR_HEDELEGH};
    `endif
    }

    vuscsr_name: coverpoint ins.current.insn[31:20] {
        bins sstatus = {CSR_SSTATUS};
        bins sie = {CSR_SIE};
        bins stvec = {CSR_STVEC};
        bins sscratch = {CSR_SSCRATCH};
        bins sepc = {CSR_SEPC};
        bins scause = {CSR_SCAUSE};
        bins stval = {CSR_STVAL};
        bins sip = {CSR_SIP};
        bins satp = {CSR_SATP};
        bins vsstatus = {CSR_VSSTATUS};
        bins vsie = {CSR_VSIE};
        bins vstvec = {CSR_VSTVEC};
        bins vsscratch = {CSR_VSSCRATCH};
        bins vsepc = {CSR_VSEPC};
        bins vscause = {CSR_VSCAUSE};
        bins vstval = {CSR_VSTVAL};
        bins vsip = {CSR_VSIP};
        bins vsatp = {CSR_VSATP};
        bins scounteren = {CSR_SCOUNTEREN};
        bins senvcfg = {CSR_SENVCFG};
        bins scountinhibit = {CSR_SCOUNTINHIBIT};
    }

    cp_hcsr_inaccessible: cross priv_mode_vu, csr_op, hcsr_name;
    `ifdef UDB_MXLEN_64
        cp_illegalupper: cross priv_mode_vu, csr_op, hhalf_name;
    `endif
    cp_scsr: cross priv_mode_vu, csr_op, vuscsr_name;

endgroup

covergroup H_inst_cg with function sample(ins_t ins);
    option.per_instance = 0;
    `include "general/RISCV_coverage_standard_coverpoints.svh"

    hlv_instr: coverpoint ins.current.insn {
        bins hlv_b = {HLV_B};
        bins hlv_bu = {HLV_BU};
        bins hlv_h = {HLV_H};
        bins hlv_hu = {HLV_HU};
        bins hlv_w = {HLV_W};
        bins hlv_wu = {HLV_WU};
    `ifdef UDB_MXLEN_64
        bins hlv_d = {HLV_D};
    `endif
    }

    hlvx_instr: coverpoint ins.current.insn {
        bins hlvx_hu = {HLVX_HU};
        bins hlvx_wu = {HLVX_WU};
    }

    hsv_instr: coverpoint ins.current.insn {
        bins hsv_b = {HSV_B};
        bins hsv_h = {HSV_H};
        bins hsv_w = {HSV_W};
    `ifdef UDB_MXLEN_64
        bins hsv_d = {HSV_D};
    `endif
    }

    hfence_instr: coverpoint ins.current.insn {
        bins hfence_gvma = {HFENCE_GVMA};
        bins hfence_vvma = {HFENCE_VVMA};
    }

    sfence_instr: coverpoint ins.current.insn {
        bins sfence_vma = {SFENCE_VMA};
    }

    mret_instr: coverpoint ins.current.insn {
        bins mret = {MRET};
    }

    sret_instr: coverpoint ins.current.insn {
        bins sret = {SRET};
    }

    mstatus_mpp: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "mstatus", "mpp") {
        bins machine = {2'b11};
        bins supervisor = {2'b01};
        bins user = {2'b00};
    }

    mstatus_mpv: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "mstatus", "mpv")[0] {
        bins clear = {0};
        bins set = {1};
    }

    mstatus_mpie: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "mstatus", "mpie")[0] {
        bins clear = {0};
        bins set = {1};
    }

    hstatus_spv: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "hstatus", "spv")[0] {
        bins clear = {0};
        bins set = {1};
    }

    hstatus_vtvm: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "hstatus", "vtvm")[0] {
        bins clear = {0};
        bins set = {1};
    }

    hstatus_vtsr: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "hstatus", "vtsr")[0] {
        bins clear = {0};
        bins set = {1};
    }

    sstatus_spp: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "sstatus", "spp")[0] {
        bins user = {0};
        bins supervisor = {1};
    }

    sstatus_spie: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "sstatus", "spie")[0] {
        bins clear = {0};
        bins set = {1};
    }

    mstatus_tvm: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "mstatus", "tvm")[0] {
        bins clear = {0};
        bins set = {1};
    }

    hstatus_hu: coverpoint get_csr_val(ins.hart, ins.issue, `SAMPLE_BEFORE, "hstatus", "hu")[0] {
        bins clear = {0};
        bins set = {1};
    }

    cp_hlv: cross priv_mode_m_s_u, hlv_instr, hstatus_hu;
    cp_hlvx: cross priv_mode_m_s_u, hlvx_instr, hstatus_hu;
    cp_hsv: cross priv_mode_m_s_u, hsv_instr, hstatus_hu;
    cp_hfence: cross priv_mode_m_s, hfence_instr, mstatus_tvm, hstatus_vtvm;
    cp_sfence: cross priv_mode_m_hs_vs, sfence_instr, mstatus_tvm, hstatus_vtvm;
    cp_mret_m: cross priv_mode_m, mret_instr, mstatus_mpp, mstatus_mpv, mstatus_mpie;
    cp_mret_illegal: cross priv_mode_hs_vs_vu, mret_instr;
    cp_sret_illegal: cross priv_mode_vu, sret_instr;
    cp_sret_m: cross priv_mode_m, sret_instr, hstatus_spv, sstatus_spp, sstatus_spie;
    cp_sret_hs: cross priv_mode_hs, sret_instr, hstatus_spv, sstatus_spp, sstatus_spie;
    cp_sret_vs: cross priv_mode_vs, sret_instr, hstatus_vtsr, sstatus_spp, sstatus_spie;

endgroup

function void h_sample(int hart, int issue, ins_t ins);
    H_mcsr_cg.sample(ins);
    H_hscsr_cg.sample(ins);
    H_vscsr_cg.sample(ins);
    H_ucsr_cg.sample(ins);
    H_vucsr_cg.sample(ins);
    H_inst_cg.sample(ins);
endfunction
