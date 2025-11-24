# SPLITS DATASET MENTAH KE FINAL

import os
import shutil
import random
import numpy as np

# ================= KONFIGURASI =================
# Path folder sumber (sesuaikan dengan nama folder Anda)
source_paths = {
    'megamendung': 'batik_m_resized', 
    'parang': 'batik_p_resized'
}

# Nama folder tujuan (akan dibuat otomatis)
base_dir = 'dataset_final'

# Rasio pembagian (Total harus 1.0)
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

# Sub-kategori yang ada di dalam folder sumber
subfolders = ['aksesoris', 'atasan', 'bawahan', 'polos']

# ================= FUNGSI UTAMA =================
def split_dataset():
    # 1. Bersihkan/Buat folder tujuan
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir) # Hapus jika sudah ada biar bersih
    
    # Buat struktur folder: dataset_final/{train,val,test}/{megamendung,parang}
    for split in ['train', 'val', 'test']:
        for category in ['megamendung', 'parang']:
            os.makedirs(os.path.join(base_dir, split, category))

    print(f"Struktur folder '{base_dir}' berhasil dibuat.\nMulai menyalin gambar...")

    # 2. Loop untuk setiap Kelas (Megamendung/Parang)
    for class_name, source_dir in source_paths.items():
        
        # 3. Loop untuk setiap Sub-kategori (Aksesoris, dll) agar RATA
        for sub in subfolders:
            current_path = os.path.join(source_dir, sub)
            
            # Cek apakah folder ada
            if not os.path.exists(current_path):
                print(f"Warning: Folder {current_path} tidak ditemukan, dilewati.")
                continue
                
            # Ambil semua file gambar
            files = [f for f in os.listdir(current_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            random.shuffle(files) # Acak urutan
            
            # Hitung jumlah pemotongan
            total_files = len(files)
            train_count = int(total_files * train_ratio)
            val_count = int(total_files * val_ratio)
            # Sisanya masuk ke test
            
            # Bagi file list
            train_files = files[:train_count]
            val_files = files[train_count:train_count + val_count]
            test_files = files[train_count + val_count:]
            
            # Fungsi helper untuk copy file
            def copy_files(file_list, split_type):
                dest_dir = os.path.join(base_dir, split_type, class_name)
                for f in file_list:
                    src = os.path.join(current_path, f)
                    
                    # PENTING: Rename file agar tidak bentrok (misal: aksesoris_gambar1.jpg)
                    new_filename = f"{sub}_{f}"
                    dst = os.path.join(dest_dir, new_filename)
                    
                    shutil.copyfile(src, dst)

            # Eksekusi copy
            copy_files(train_files, 'train')
            copy_files(val_files, 'val')
            copy_files(test_files, 'test')
            
            print(f"[{class_name} - {sub}] Split: Train={len(train_files)}, Val={len(val_files)}, Test={len(test_files)}")

    print("\n✅ Pembagian Data Selesai!")
    print(f"Total gambar Test tersebar merata dari aksesoris, atasan, bawahan, dan polos.")

# Jalankan script
split_dataset()