import csv, os

FILE = "data_barang.csv"
HEADER = ["id", "nama", "kategori", "stok"]

# ================= LINKED LIST =================
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def tampil(self):
        data = []
        cur = self.head
        while cur:
            data.append(cur.data)
            cur = cur.next
        return data

    def cari(self, id_barang):
        cur = self.head
        while cur:
            if cur.data["id"] == id_barang:
                return cur.data
            cur = cur.next
        return None

    def hapus(self, id_barang):
        cur = self.head
        prev = None

        while cur:
            if cur.data["id"] == id_barang:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                return True

            prev = cur
            cur = cur.next

        return False


# ================= QUEUE =================
class Queue:
    def __init__(self):
        self.data = []

    def enqueue(self, barang):
        self.data.append(barang)

    def dequeue(self):
        if self.data:
            return self.data.pop(0)
        return None

    def tampil(self):
        return self.data


# ================= CSV =================
def load_csv(ll):
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
        return

    with open(FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ll.tambah(row)

def save_csv(ll):
    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(ll.tampil())


# ================= FITUR =================
def generate_id(ll):
    return "BRG" + str(len(ll.tampil()) + 1).zfill(3)

def tambah_barang(ll):
    data = {
        "id": generate_id(ll),
        "nama": input("Nama Barang : "),
        "kategori": input("Kategori    : "),
        "stok": input("Stok        : ")
    }

    ll.tambah(data)
    save_csv(ll)
    print("Barang berhasil ditambahkan!")

def lihat_barang(ll):
    data = ll.tampil()

    if not data:
        print("Data barang kosong.")
    else:
        print("\n=== DATA BARANG ===")
        for b in data:
            print(b["id"], "-", b["nama"], "-", b["kategori"], "- Stok:", b["stok"])

def cari_barang(ll):
    id_barang = input("Masukkan ID barang: ")
    barang = ll.cari(id_barang)

    if barang:
        print("Ditemukan:", barang)
    else:
        print("Barang tidak ditemukan.")

def update_barang(ll):
    id_barang = input("Masukkan ID barang: ")
    barang = ll.cari(id_barang)

    if barang:
        barang["nama"] = input("Nama baru     : ")
        barang["kategori"] = input("Kategori baru : ")
        barang["stok"] = input("Stok baru     : ")

        save_csv(ll)
        print("Data barang berhasil diupdate!")
    else:
        print("Barang tidak ditemukan.")

def hapus_barang(ll):
    id_barang = input("Masukkan ID barang: ")

    if ll.hapus(id_barang):
        save_csv(ll)
        print("Data barang berhasil dihapus!")
    else:
        print("Barang tidak ditemukan.")

def sorting_barang(ll):
    data = ll.tampil()
    data.sort(key=lambda x: x["nama"])

    print("\nHasil sorting berdasarkan nama barang:")
    for b in data:
        print(b["id"], "-", b["nama"], "-", b["kategori"], "- Stok:", b["stok"])

def antrean_barang_masuk(ll, q):
    id_barang = input("Masukkan ID barang yang akan diproses: ")
    barang = ll.cari(id_barang)

    if barang:
        q.enqueue(barang)
        print("Barang masuk ke antrean proses inventori.")
    else:
        print("Barang tidak ditemukan.")

def proses_barang(q):
    barang = q.dequeue()

    if barang:
        print("Barang sedang diproses:", barang["nama"])
    else:
        print("Antrean barang kosong.")


# ================= MAIN PROGRAM =================
def main():
    ll = LinkedList()
    q = Queue()

    load_csv(ll)

    while True:
        print("\n=== SISTEM INVENTORI BARANG ===")
        print("1. Tambah Barang")
        print("2. Lihat Barang")
        print("3. Cari Barang")
        print("4. Update Barang")
        print("5. Hapus Barang")
        print("6. Sorting Barang")
        print("7. Tambah Antrean Barang")
        print("8. Proses Barang")
        print("9. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_barang(ll)
        elif pilih == "2":
            lihat_barang(ll)
        elif pilih == "3":
            cari_barang(ll)
        elif pilih == "4":
            update_barang(ll)
        elif pilih == "5":
            hapus_barang(ll)
        elif pilih == "6":
            sorting_barang(ll)
        elif pilih == "7":
            antrean_barang_masuk(ll, q)
        elif pilih == "8":
            proses_barang(q)
        elif pilih == "9":
            save_csv(ll)
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid!")


main()