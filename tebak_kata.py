import random
import time
import os

class TebakKataGame:
    def __init__(self):
        self.categories = {
            "buah": ["apel", "mangga", "jeruk", "pisang", "anggur", "nanas", "semangka", "durian", "rambutan", "alpukat"],
            "hewan": ["kucing", "anjing", "gajah", "harimau", "kuda", "kelinci", "burung", "ikan", "singa", "jerapah"],
            "negara": ["indonesia", "malaysia", "jepang", "korea", "china", "inggris", "jerman", "prancis", "brazil", "australia"],
            "kota": ["jakarta", "bandung", "surabaya", "yogyakarta", "semarang", "medan", "makassar", "palembang", "denpasar", "malang"]
        }
        self.score = 0
        self.high_score = self.load_high_score()
        self.play_count = 0
        self.start_time = 0
        
    def clear_screen(self):
        """Membersihkan layar terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def load_high_score(self):
        """Memuat high score dari file."""
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except:
            return 0
            
    def save_high_score(self):
        """Menyimpan high score ke file."""
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))
            
    def acak_kata(self, kata):
        """Pengacakan huruf dalam kata."""
        kata_list = list(kata)
        random.shuffle(kata_list)
        return ''.join(kata_list)
        
    def pilih_kategori(self):
        """Menampilkan pilihan kategori dan meminta input dari pemain."""
        self.clear_screen()
        print("\n=== PILIH KATEGORI ===")
        for idx, category in enumerate(self.categories.keys(), 1):
            print(f"{idx}. {category.title()}")
        
        while True:
            try:
                choice = int(input("\nPilih kategori (1-4): "))
                if 1 <= choice <= 4:
                    return list(self.categories.keys())[choice - 1]
                else:
                    print("Pilihan tidak valid. Silakan pilih angka 1-4.")
            except ValueError:
                print("Masukkan angka!")
                
    def tampilkan_banner(self):
        """Menampilkan banner permainan."""
        self.clear_screen()
        print("""
        ╔════════════════════════════════════════╗
        ║         PERMAINAN TEBAK KATA           ║
        ╚════════════════════════════════════════╝
        """)
        print(f"High Score: {self.high_score}")
        print(f"Score saat ini: {self.score}")
        
    def mulai_permainan(self):
        """Memulai permainan."""
        self.score = 0
        self.play_count = 0
        
        while True:
            kategori = self.pilih_kategori()
            kata_list = self.categories[kategori]
            
            for _ in range(5):  # Mainkan 5 kata per kategori
                self.play_count += 1
                self.tampilkan_banner()
                print(f"\nKategori: {kategori.upper()}")
                
                # Pilih kata acak dan acak hurufnya
                kata_asli = random.choice(kata_list)
                kata_list.remove(kata_asli)  # Hindari pengulangan kata
                kata_acak = self.acak_kata(kata_asli)
                
                # Pastikan kata teracak berbeda dengan aslinya
                while kata_acak == kata_asli and len(kata_asli) > 1:
                    kata_acak = self.acak_kata(kata_asli)
                
                # Tampilkan kata acak dan mulai timer
                print(f"\nTebak kata ini: {kata_acak.upper()}")
                self.start_time = time.time()
                
                # Coba tebak
                for attempt in range(3, 0, -1):
                    tebakan = input(f"\nMasukkan tebakan Anda ({attempt} kesempatan): ").lower()
                    
                    if tebakan == kata_asli:
                        waktu_tebak = time.time() - self.start_time
                        bonus = max(0, int(30 - waktu_tebak)) * 2
                        points = 100 + bonus
                        
                        print(f"\n✓ BENAR! Kata yang tepat adalah: {kata_asli.upper()}")
                        print(f"Waktu: {waktu_tebak:.2f} detik")
                        print(f"Poin: 100 + bonus kecepatan {bonus} = {points}")
                        
                        self.score += points
                        time.sleep(2)
                        break
                    else:
                        print("✗ Salah! Coba lagi...")
                
                if tebakan != kata_asli:
                    print(f"\nMaaf, kata yang benar adalah: {kata_asli.upper()}")
                    time.sleep(2)
                
                # Jika kata dalam kategori habis, keluar dari loop
                if not kata_list:
                    break
            
            # Cek dan update high score
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
                print("\n🎉 SELAMAT! Anda mendapatkan HIGH SCORE baru!")
            
            lanjut = input("\nIngin main lagi? (y/n): ").lower()
            if lanjut != 'y':
                self.tampilkan_hasil()
                
                break
    
    def tampilkan_hasil(self):
        """Menampilkan hasil akhir permainan."""
        self.clear_screen()
        print("\n=== HASIL PERMAINAN ===")
        print(f"Score Akhir: {self.score}")
        print(f"High Score: {self.high_score}")
        print(f"Jumlah kata yang ditebak: {self.play_count}")
        print("\nTerima kasih telah bermain!")
        
if __name__ == "__main__":
    game = TebakKataGame()
    game.tampilkan_banner()
    print("\nSelamat datang di permainan Tebak Kata!")
    print("Aturan: Tebak kata yang teracak dalam batas waktu untuk mendapatkan poin.")
    print("Semakin cepat Anda menebak, semakin banyak poin bonus!")
    input("\nTekan Enter untuk mulai...")
    game.mulai_permainan()
