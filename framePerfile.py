import os
import shutil

import cv2
from tqdm import tqdm  # Library untuk progress bar (pip install tqdm)


def extract_frames(video_path, output_folder):
    # 1. Buat folder jika belum ada

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

        print(f"Folder '{output_folder}' dibuat.")

    # 2. Buka video

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Tidak bisa membuka video.")

        return

    # 3. Ambil info video

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fps = cap.get(cv2.CAP_PROP_FPS)

    print(f"Mulai ekstraksi: {total_frames} frames terdeteksi.")

    print(f"FPS: {fps}")

    # 4. Loop ekstraksi dengan Progress Bar

    count = 0

    # tqdm membuat tampilan loading bar

    pbar = tqdm(total=total_frames, unit="frame")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Simpan file (format 0001.png, 0002.png, dst agar urut)

        filename = os.path.join(output_folder, f"frame_{count + 1:05d}.png")

        cv2.imwrite(filename, frame)

        count += 1

        pbar.update(1)  # Update progress bar

    cap.release()

    pbar.close()

    # Cek apakah berhenti lebih awal

    if count < total_frames:
        print(
            f"\n⚠️ Peringatan: Ekstraksi berhenti lebih awal di frame {count} (dari total {total_frames})."
        )

        print(
            "Penyebab: File video mungkin korup di titik ini atau metadata durasi video salah."
        )

        print("Frame yang berhasil diambil tetap diamankan.")

    else:
        print(
            f"\n✅ Selesai sempurna! {count} frame tersimpan di folder '{output_folder}'."
        )

    # 5. Otomatis Zip folder agar mudah didownload/dipindah

    print("Sedang mengompres folder menjadi .zip ...")

    shutil.make_archive(output_folder, "zip", output_folder)

    print(f"📦 File ZIP siap: {output_folder}.zip")


# --- Konfigurasi ---

video_file = "videoplayback.mp4"  # Ganti dengan nama videomu

folder_name = "frames_urva_Jawanicus_Muaniritus"


# Jalankan fungsi

extract_frames(video_file, folder_name)


