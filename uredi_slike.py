import json
from json import JSONDecodeError
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"


def uredi():
    print("Uređujem")


def validate_work_dir(root):
    if not CONFIG_FILE.exists():
        messagebox.showerror(
            "Greška",
            "Ne mogu naći config.json.\nDodajte osnovnu mapu u postavkama.",
            parent=root,
        )
        return None

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            if not isinstance(config, dict):
                raise ValueError()
    except (JSONDecodeError, ValueError):
        messagebox.showerror(
            "Greška",
            "config.json je neispravan.\nDodajte osnovnu mapu u postavkama.",
            parent=root,
        )
        return None
    except OSError:
        messagebox.showerror(
            "Greška",
            "Došlo je do greške prilikom učitavanja config.json file-a.",
            parent=root,
        )
        return None

    if "work_dir" not in config:
        messagebox.showerror(
            "Greška",
            "U config.json-u nedostaje work_dir postavka.\nDodajte osnovnu mapu u postavkama.",
            parent=root,
        )
        return None

    work_dir_value = config.get("work_dir")
    if not isinstance(work_dir_value, str) or not work_dir_value:
        messagebox.showerror(
            "Greška",
            "work_dir postavka ima neispravnu vrijednost.\nDodajte ispravnu mapu u postavkama.",
            parent=root,
        )
        return None

    work_dir = Path(work_dir_value)
    if not work_dir.exists() or not work_dir.is_dir():
        messagebox.showerror(
            "Greška",
            f"Ne mogu pronaći mapu:\n{work_dir}\nDodajte ispravnu mapu u postavkama.",
            parent=root,
        )
        return None

    return work_dir


def start_gui():
    root = tk.Tk()
    root.title("Uredi slike")

    # SKU
    lbl_sku = tk.Label(root, text="SKU:")
    lbl_sku.grid(column=0, row=0, sticky="w", padx=5, pady=5)

    txt_sku = tk.Entry(root, width=10)
    txt_sku.grid(column=1, row=0, sticky="w", padx=5, pady=5)
    txt_sku.focus_set()

    # Web naziv
    lbl_name = tk.Label(root, text="WEB naziv:")
    lbl_name.grid(column=0, row=1, sticky="w", padx=5, pady=5)

    txt_name = tk.Entry(root, width=100)
    txt_name.grid(column=1, row=1, sticky="w", padx=5, pady=5)

    # Button Uredi
    btn_uredi = tk.Button(
        root, text="Uredi", width=10, command=uredi, state=tk.DISABLED
    )
    btn_uredi.grid(column=1, row=2, sticky="e", padx=5, pady=5)

    # open_settings dialog
    def open_settings():
        popup = tk.Toplevel(root)
        popup.title("Odabir osnovne mape")
        popup.resizable(False, False)
        popup.transient(root)
        popup.grab_set()
        lbl_info = tk.Label(popup, text="Odaberite osnovnu mapu proizvoda:")
        lbl_info.grid(column=0, row=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        txt_work_dir = tk.Entry(popup, width=60)
        txt_work_dir.grid(column=0, row=1, columnspan=2, sticky="w", padx=10, pady=5)

        # Button Odaberi...
        def choose_folder():
            folder = filedialog.askdirectory(
                title="Odaberi osnovnu mapu",
                parent=popup,
            )

            if folder:
                txt_work_dir.delete(0, tk.END)
                txt_work_dir.insert(0, folder)

        btn_choose = tk.Button(
            popup,
            text="Odaberi...",
            command=choose_folder,
            width=12,
        )
        btn_choose.grid(column=2, row=1, sticky="w", padx=(0, 10), pady=5)

        # Button Spremi
        def save():
            nonlocal work_dir
            work_dir_string = txt_work_dir.get().strip()
            if not work_dir_string:
                messagebox.showerror(
                    "Greška",
                    "Dodajte ispravnu mapu u postavkama.",
                    parent=popup,
                )
                return

            new_work_dir = Path(work_dir_string)
            if not new_work_dir.exists() or not new_work_dir.is_dir():
                messagebox.showerror(
                    "Greška",
                    f"Ne mogu pronaći mapu:\n{new_work_dir}\nDodajte ispravnu mapu u postavkama.",
                    parent=popup,
                )
                return

            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    if not isinstance(config, dict):
                        config = {}
            except (FileNotFoundError, JSONDecodeError, OSError):
                config = {}

            config["work_dir"] = str(new_work_dir)

            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(config, f, ensure_ascii=False, indent=4)
            except OSError:
                messagebox.showerror(
                    "Greška",
                    "Došlo je do greške prilikom spremanja config.json file-a.",
                    parent=popup,
                )
                return

            work_dir = new_work_dir
            popup.destroy()

        btn_save = tk.Button(
            popup,
            text="Spremi",
            command=save,
            width=10,
        )
        btn_save.grid(column=0, row=2, sticky="e", padx=10, pady=10)

        # Button Odustani
        btn_cancel = tk.Button(
            popup,
            text="Odustani",
            command=popup.destroy,
            width=10,
        )
        btn_cancel.grid(column=1, row=2, sticky="w", padx=(0, 10), pady=10)

        # Postavljanje txtboxa
        txt_work_dir.focus_set()

        if work_dir:
            txt_work_dir.insert(0, str(work_dir))

    # Menu
    mnu_bar = tk.Menu(root)

    mnu_postavke = tk.Menu(mnu_bar, tearoff=0)
    mnu_postavke.add_command(label="Osnovna mapa", command=open_settings)

    mnu_bar.add_cascade(label="Postavke", menu=mnu_postavke)
    root.config(menu=mnu_bar)

    # config.json provjere
    root.update()
    work_dir = validate_work_dir(root)

    root.mainloop()


def main():
    start_gui()


if __name__ == "__main__":
    main()
