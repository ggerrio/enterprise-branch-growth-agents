import asyncio
import sys
import json
from rich.console import Console
from rich.panel import Panel

console = Console()

# Simulasi database Server MCP
DATABASE = [
    {"Nama_Showroom": "Showroom_Garuda_Motor", "Booking_Volume_Bulan_Lalu": 50, "Booking_Volume_Bulan_Ini": 35, "NPL_Persen": 1.2, "Nama_CMO_Handler": "Budi_Santoso"},
    {"Nama_Showroom": "Showroom_Maju_Jaya", "Booking_Volume_Bulan_Lalu": 30, "Booking_Volume_Bulan_Ini": 28, "NPL_Persen": 0.8, "Nama_CMO_Handler": "Siti_Aminah"},
    {"Nama_Showroom": "Showroom_Raya_Automobil", "Booking_Volume_Bulan_Lalu": 40, "Booking_Volume_Bulan_Ini": 20, "NPL_Persen": 3.5, "Nama_CMO_Handler": "Iwan_Setiawan"},
    {"Nama_Showroom": "Showroom_Berkat_Mobilindo", "Booking_Volume_Bulan_Lalu": 25, "Booking_Volume_Bulan_Ini": 24, "NPL_Persen": 1.5, "Nama_CMO_Handler": "Budi_Santoso"},
    {"Nama_Showroom": "Showroom_Tunas_Harapan", "Booking_Volume_Bulan_Lalu": 15, "Booking_Volume_Bulan_Ini": 5, "NPL_Persen": 4.2, "Nama_CMO_Handler": "Siti_Aminah"}
]

def human_in_the_loop_approval(showroom: str, dana_usulan: str) -> bool:
    console.print("\n")
    console.print(Panel(
        f"[bold red]⚠️ PERMINTAAN PERSETUJUAN DANA STRATEGIS KELUAR[/bold red]\n\n"
        f"🚨 [bold]Showroom Target:[/bold] {showroom}\n"
        f"💰 [bold]Usulan Subsidi Bunga:[/bold] {dana_usulan}\n\n"
        f"Apakah Anda menyetujui pencairan dana promosi cabang ini?",
        title="[BCAF SECURITY GUARD]", border_style="red"
    ))
    pilihan = console.input("[bold yellow]Ketik (Y untuk Setuju / N untuk Tolak): [/bold yellow]").strip().upper()
    return pilihan == "Y"

async def main_loop():
    console.print(Panel(
        "[bold green]BCAF Branch Growth Strategy Agent - Local Sandbox Active v1.0.0[/bold green]\n"
        "Sistem Mode Sandbox Lokal (Bypass Server 503). Siap digunakan untuk verifikasi Trajectory.\n"
        "Ketik 'exit' atau 'quit' untuk keluar.",
        title="[BCA FINANCE AI SYSTEM - MOCK]", border_style="yellow"
    ))

    while True:
        try:
            user_prompt = console.input("\n[bold blue]Branch Manager 🤵 ──> [/bold blue]").strip()
            if not user_prompt or user_prompt.lower() in ["exit", "quit"]:
                break
            
            with console.status("[bold green]Mengaktifkan MCP Client & Membaca Dokumen SKILL.md...[/bold green]"):
                await asyncio.sleep(1.5) # Simulasi delay berpikir
            
            # Skenario 1: Prompt Analisis Umum
            if "analisis" in user_prompt.lower() or "penurunan" in user_prompt.lower():
                console.print("\n[bold green][AI AGENT RESPONSE][/bold green]")
                console.print("Membaca database cabang via MCP Server... [✔ SUCCESS]")
                console.print("Ditemukan showroom dengan penurunan volume penjualan > 10%:\n")
                
                console.print("[1] Showroom_Garuda_Motor (Volume drop 30%, NPL: 1.2% - AMAN)")
                console.print("[2] Showroom_Raya_Automobil (Volume drop 50%, NPL: 3.5% - BAHAYA / DIBLOKIR)")
                console.print("[3] Showroom_Tunas_Harapan (Volume drop 66%, NPL: 4.2% - BAHAYA / DIBLOKIR)\n")
                
                console.print("Memformulasikan draf subsidi komisi bunga taktis untuk showroom yang lolos kriteria aman...")
                
                # Memicu Intervensi HITL untuk Garuda Motor
                is_approved = human_in_the_loop_approval("Showroom_Garuda_Motor", "Rp 25.000.000")
                if is_approved:
                    console.print("\n[bold green]STATUS: APPROVED.[/bold green] Dana promosi Rp 25.000.000 dikunci untuk Showroom Garuda Motor. Program CMO lapangan diaktifkan.")
                else:
                    console.print("\n[bold red]STATUS: REJECTED.[/bold red] Alokasi anggaran dibatalkan oleh Branch Manager. Keamanan keuangan cabang tetap terjaga.")
            
            # Skenario 2: Prompt Showroom Bermasalah (Raya Automobil)
            elif "raya automobil" in user_prompt.lower():
                console.print("\n[bold green][AI AGENT RESPONSE][/bold green]")
                console.print("Mengevaluasi data showroom: [bold]Showroom_Raya_Automobil[/bold]")
                console.print("[bold red]🚨 PENOLAKAN OTOMATIS ATURAN SKILL.MD (GATE 3):[/bold red]")
                console.print("Maaf, permintaan program subsidi ditolak. Angka NPL showroom tersebut berada di 3.5% (melebihi batas toleransi cabang maks 2.0%).")
            
            else:
                console.print("\n[bold yellow]Agen mengerti konteks Anda, namun jalankan skenario simulasi 'Analisis penurunan mobil bekas' atau ketik nama showroom spesifik untuk demo video.[/bold yellow]")
                
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    asyncio.run(main_loop())