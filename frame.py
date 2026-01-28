import os
import shutil

import cv2
from tqdm import tqdm


def extract_frames_from_folder(source_folder, root_output_folder):
    # 1. Cek apakah folder sumber ada
    if not os.path.exists(source_folder):
        print(f"❌ Error: Folder sumber '{source_folder}' tidak ditemukan.")
        return

    # 2. Buat folder output utama jika belum ada
    if not os.path.exists(root_output_folder):
        os.makedirs(root_output_folder)

    # 3. Ambil daftar semua file .mp4 di folder sumber
    video_files = [
        f for f in os.listdir(source_folder) if f.endswith(".mp4") or f.endswith(".MP4")
    ]

    if not video_files:
        print("❌ Tidak ada file MP4 ditemukan di folder tersebut.")
        return

    print(f"📂 Ditemukan {len(video_files)} video. Mulai memproses...\n")

    # 4. Loop untuk setiap video
    for video_name in video_files:
        video_path = os.path.join(source_folder, video_name)

        # Buat nama folder khusus untuk video ini (tanpa ekstensi .mp4)
        video_name_no_ext = os.path.splitext(video_name)[0]
        current_output_folder = os.path.join(root_output_folder, video_name_no_ext)

        # Buat folder khusus video ini
        if not os.path.exists(current_output_folder):
            os.makedirs(current_output_folder)

        print(f"🎬 Sedang memproses: {video_name}")

        # --- Proses Ekstraksi OpenCV ---
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"   ⚠️ Gagal membuka {video_name}, melewati file ini.")
            continue

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        count = 0
        pbar = tqdm(
            total=total_frames, unit="frame", desc=video_name_no_ext, leave=False
        )

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Simpan frame: folder_output/nama_video/frame_00001.png
            filename = os.path.join(current_output_folder, f"frame_{count + 1:05d}.png")
            cv2.imwrite(filename, frame)

            count += 1
            pbar.update(1)

        cap.release()
        pbar.close()
        print(f"   ✅ Selesai: {count} frame disimpan di '{video_name_no_ext}/'\n")

    # 5. Setelah SEMUA video selesai, baru di-ZIP
    print("-" * 30)
    print("📦 Sedang membuat file ZIP gabungan...")

    # Format zip: nama_zip, format, folder_yang_mau_dizip
    shutil.make_archive(root_output_folder, "zip", root_output_folder)

    print(f"🎉 SUKSES! Semua frame telah disatukan di: {root_output_folder}.zip")


# --- KONFIGURASI ---
# Sesuaikan nama folder dengan struktur di gambar kamu
SOURCE_FOLDER = "dari sulton"  # Folder tempat video .mp4 berada
OUTPUT_FOLDER = "hasil_ekstraksi_all"  # Nama folder & nama file zip output

# Jalankan Program
if __name__ == "__main__":
    extract_frames_from_folder(SOURCE_FOLDER, OUTPUT_FOLDER)
