import heapq
import random
import time
from concurrent.futures import ProcessPoolExecutor


def urutkan_potongan(data: list[int]) -> list[int]:
  return sorted(data)


def jalan_serial(data: list[int]) -> tuple[list[int], float]:
  awal = time.perf_counter()
  hasil = sorted(data)
  durasi = time.perf_counter() - awal
  return hasil, durasi


def jalan_paralel(
    data: list[int], jumlah_worker: int
) -> tuple[list[int], float]:
  awal = time.perf_counter()
  n = len(data)
  ukuran_blok = max(1, n // jumlah_worker)
  potongan = [
      data[i * ukuran_blok : (n if i == jumlah_worker - 1 else (i + 1) * ukuran_blok)]
      for i in range(jumlah_worker)
  ]

  with ProcessPoolExecutor(max_workers=jumlah_worker) as executor:
    potongan_terurut = list(executor.map(urutkan_potongan, potongan))

  # Menggabungkan semua potongan yang sudah terurut
  hasil = list(heapq.merge(*potongan_terurut))
  durasi = time.perf_counter() - awal
  return hasil, durasi


if __name__ == "__main__":
  JUMLAH_DATA = 3_000_000
  rng = random.Random(42)
  data_acak = [rng.randint(1, 10_000_000) for _ in range(JUMLAH_DATA)]

  hasil_s, waktu_s = jalan_serial(data_acak)
  print(f"Serial       -> Waktu: {waktu_s:.4f} detik")

  for workers in [2, 4]:
    hasil_p, waktu_p = jalan_paralel(data_acak, workers)
    sama = hasil_s == hasil_p
    speedup = waktu_s / waktu_p if waktu_p > 0 else 0
    print(
        f"Paralel ({workers}w) -> Waktu: {waktu_p:.4f} detik | Speedup:"
        f" {speedup:.2f}x | Hasil sama: {sama}"
    )