
# ============================================================
# STEP 1: IMPORT LIBRARIES

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import os

# ============================================================
# STEP 2: CREATE TEXT FILES IF THEY DO NOT EXIST

def initialize_files():
    """Create the data files if they don't already exist."""
    for filename in ["vehicles.txt", "customers.txt", "rentals.txt"]:
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                pass  # Just create the file, leave it empty

# Call this function immediately so files are ready before anything else
initialize_files()


# ============================================================
# STEP 3: CREATE THE VEHICLE BASE CLASS (Parent Class)

class Vehicle:
    """Base class for all vehicles. Contains common attributes and methods."""

    def __init__(self, vehicle_id, name, rent_per_day, is_available=True):
        # __init__ is the CONSTRUCTOR - it runs automatically when we create an object
        # 'self' refers to the current object being created

        # Using ENCAPSULATION: we use single underscore _ to indicate
        # these are "protected" attributes (not directly changed from outside)
        self._vehicle_id   = vehicle_id
        self._name         = name
        self._rent_per_day = float(rent_per_day)
        self._is_available = is_available  # True = available, False = rented

    # ---------- GETTER methods (to read private data safely) ----------

    def get_id(self):
        """Return the vehicle ID."""
        return self._vehicle_id

    def get_name(self):
        """Return the vehicle name."""
        return self._name

    def get_rent_per_day(self):
        """Return the rent per day."""
        return self._rent_per_day

    def get_availability(self):
        """Return True if available, False if rented."""
        return self._is_available

    # ---------- SETTER methods (to change private data safely) ----------

    def set_availability(self, status):
        """Change availability: True = available, False = rented."""
        self._is_available = status

    # ---------- Other methods ----------

    def get_type(self):
        """Return the vehicle type. Subclasses will override this."""
        return "Vehicle"

    def get_display_info(self):
        """Return basic info as a list for displaying in the table."""
        status = "Available" if self._is_available else "Rented"
        return [self._vehicle_id, self._name, self._rent_per_day, status]

    def to_file_string(self):
        """
        Convert this vehicle's data into one line of text for saving to file.
        Subclasses (Car, Bike) will override this method.
        """
        return ""


# ============================================================
# STEP 4: CREATE THE CAR SUBCLASS (Child Class of Vehicle)
# Car INHERITS from Vehicle using: class Car(Vehicle)
# Car has 2 extra attributes that only cars have:
#   - seats    : Number of seats (e.g., 5)
#   - fuel_type: "Petrol", "Diesel", or "Electric"
# ============================================================

class Car(Vehicle):
    """Car class - inherits from Vehicle. Has extra: seats and fuel_type."""

    def __init__(self, vehicle_id, name, rent_per_day, seats, fuel_type, is_available=True):
        # Call the PARENT class constructor using super()
        # This sets vehicle_id, name, rent_per_day, is_available
        super().__init__(vehicle_id, name, rent_per_day, is_available)

        # Extra attributes only for Car
        self._seats     = int(seats)
        self._fuel_type = fuel_type

    def get_type(self):
        """Return vehicle type as 'Car'."""
        return "Car"

    def get_seats(self):
        return self._seats

    def get_fuel_type(self):
        return self._fuel_type

    def get_display_info(self):
        """Return car info as a list for the display table."""
        status = "Available" if self._is_available else "Rented"
        return [self._vehicle_id, "Car", self._name,
                self._rent_per_day, self._seats, self._fuel_type, "N/A", status]

    def to_file_string(self):
        """
        Save car data as a comma-separated line.
        Format: CAR,id,name,rent,seats,fuel,availability
        """
        avail = "1" if self._is_available else "0"
        return f"CAR,{self._vehicle_id},{self._name},{self._rent_per_day},{self._seats},{self._fuel_type},{avail}\n"


# ============================================================
# STEP 5: CREATE THE BIKE SUBCLASS (Child Class of Vehicle)
# Bike also INHERITS from Vehicle.
# Bike has 1 extra attribute:
#   - engine_cc : Engine size in CC (e.g., 150, 250)
# ============================================================

class Bike(Vehicle):
    """Bike class - inherits from Vehicle. Has extra: engine_cc."""

    def __init__(self, vehicle_id, name, rent_per_day, engine_cc, is_available=True):
        # Call parent constructor
        super().__init__(vehicle_id, name, rent_per_day, is_available)

        # Extra attribute only for Bike
        self._engine_cc = int(engine_cc)

    def get_type(self):
        """Return vehicle type as 'Bike'."""
        return "Bike"

    def get_engine_cc(self):
        return self._engine_cc

    def get_display_info(self):
        """Return bike info as a list for the display table."""
        status = "Available" if self._is_available else "Rented"
        return [self._vehicle_id, "Bike", self._name,
                self._rent_per_day, "N/A", "N/A", self._engine_cc, status]

    def to_file_string(self):
        """
        Save bike data as a comma-separated line.
        Format: BIKE,id,name,rent,engine_cc,availability
        """
        avail = "1" if self._is_available else "0"
        return f"BIKE,{self._vehicle_id},{self._name},{self._rent_per_day},{self._engine_cc},{avail}\n"


# ============================================================
# STEP 6: FILE HANDLING FUNCTIONS
# These functions READ and WRITE data to the text files.
# Think of them as the "database" of our system.
# ============================================================

def load_vehicles():
    """
    Read all vehicles from vehicles.txt and return a dictionary.
    Dictionary format: { vehicle_id : Vehicle_object }
    """
    vehicles = {}
    try:
        with open("vehicles.txt", "r") as f:
            for line in f:
                line = line.strip()     # Remove spaces/newlines
                if not line:            # Skip empty lines
                    continue
                parts = line.split(",") # Split by comma

                if parts[0] == "CAR" and len(parts) == 7:
                    # CAR,id,name,rent,seats,fuel,avail
                    vid, name, rent = parts[1], parts[2], parts[3]
                    seats, fuel, avail = parts[4], parts[5], parts[6]
                    car = Car(vid, name, rent, seats, fuel, avail == "1")
                    vehicles[vid] = car

                elif parts[0] == "BIKE" and len(parts) == 6:
                    # BIKE,id,name,rent,cc,avail
                    vid, name, rent = parts[1], parts[2], parts[3]
                    cc, avail = parts[4], parts[5]
                    bike = Bike(vid, name, rent, cc, avail == "1")
                    vehicles[vid] = bike

    except FileNotFoundError:
        pass  # File doesn't exist yet, return empty dict

    return vehicles


def save_vehicles(vehicles):
    """
    Write all vehicles to vehicles.txt.
    Overwrites the file with current data.
    """
    with open("vehicles.txt", "w") as f:
        for v in vehicles.values():
            f.write(v.to_file_string())


def load_rentals():
    """
    Read all rental records from rentals.txt.
    Returns a list of dictionaries, one per rental.
    """
    rentals = []
    try:
        with open("rentals.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                # Format: rental_id, vehicle_id, customer_name, contact,
                #         days, rent_date, return_date(or ACTIVE), total_bill
                if len(parts) >= 7:
                    rental = {
                        "rental_id"   : parts[0],
                        "vehicle_id"  : parts[1],
                        "customer"    : parts[2],
                        "contact"     : parts[3],
                        "days"        : int(parts[4]),
                        "rent_date"   : parts[5],
                        "return_date" : parts[6],
                        "total_bill"  : parts[7] if len(parts) > 7 else "0"
                    }
                    rentals.append(rental)
    except FileNotFoundError:
        pass
    return rentals


def save_rentals(rentals):
    """Write all rental records to rentals.txt."""
    with open("rentals.txt", "w") as f:
        for r in rentals:
            line = (f"{r['rental_id']},{r['vehicle_id']},{r['customer']},"
                    f"{r['contact']},{r['days']},{r['rent_date']},"
                    f"{r['return_date']},{r['total_bill']}\n")
            f.write(line)


def save_customer(customer_name, contact, vehicle_id, rent_date):
    """Append a customer record to customers.txt."""
    with open("customers.txt", "a") as f:
        f.write(f"{customer_name},{contact},{vehicle_id},{rent_date}\n")


def load_customers():
    """Read all customer records from customers.txt."""
    customers = []
    try:
        with open("customers.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) >= 4:
                    customers.append({
                        "name"      : parts[0],
                        "contact"   : parts[1],
                        "vehicle_id": parts[2],
                        "rent_date" : parts[3]
                    })
    except FileNotFoundError:
        pass
    return customers


def generate_rental_id(rentals):
    """
    Auto-generate the next rental ID.
    Example: if 3 rentals exist, next ID = "R004"
    """
    return f"R{len(rentals) + 1:03d}"


# ============================================================
# STEP 7: BILLING FUNCTIONS
# These functions calculate how much a customer owes.
# ============================================================

def calculate_rental_bill(rent_per_day, days):
    """
    Basic rental bill formula:
    Total Bill = Rent Per Day × Number of Days
    (Note: project spec says 'per hour' but data model uses days;
     we treat each 'day' as the billing unit for simplicity.)
    """
    return rent_per_day * days


def calculate_late_fine(expected_days, actual_days, rent_per_day):
    """
    If customer returns the vehicle LATE, we charge a fine.
    Late Fine = Extra Days × Rent Per Day × 1.5  (50% penalty)
    Returns 0 if returned on time or early.
    """
    extra_days = actual_days - expected_days
    if extra_days > 0:
        return extra_days * rent_per_day * 1.5
    return 0.0


def apply_discount(total_bill, days):
    """
    Long rental discount:
    - Rent for 7+ days  → 10% discount
    - Rent for 14+ days → 20% discount
    - Rent for 30+ days → 30% discount
    Returns the final bill after discount.
    """
    if days >= 30:
        discount = 0.30
    elif days >= 14:
        discount = 0.20
    elif days >= 7:
        discount = 0.10
    else:
        discount = 0.0

    discounted = total_bill * (1 - discount)
    return discounted, discount * 100  # return bill and discount percentage


# ============================================================
# STEP 8: RENTAL MANAGEMENT FUNCTIONS
# These are the core business logic functions that connect
# the GUI to the file storage.
# ============================================================

def add_vehicle(vehicle_type, vid, name, rent, extra1, extra2=""):
    """
    Add a new vehicle to the system.
    - vehicle_type : "Car" or "Bike"
    - vid          : Vehicle ID (e.g., "V001")
    - name         : Vehicle name
    - rent         : Rent per day
    - extra1       : Seats (Car) or Engine CC (Bike)
    - extra2       : Fuel type (Car only)
    Returns (True, message) on success, (False, error) on failure.
    """
    vehicles = load_vehicles()

    # Check if vehicle ID already exists
    if vid in vehicles:
        return False, f"Vehicle ID '{vid}' already exists!"

    # Validate inputs
    try:
        rent_val = float(rent)
        if rent_val <= 0:
            return False, "Rent per day must be greater than 0."
    except ValueError:
        return False, "Rent per day must be a valid number."

    # Create the correct object based on type
    if vehicle_type == "Car":
        try:
            seats = int(extra1)
        except ValueError:
            return False, "Number of seats must be a whole number."
        new_vehicle = Car(vid, name, rent, seats, extra2)
    else:  # Bike
        try:
            cc = int(extra1)
        except ValueError:
            return False, "Engine CC must be a whole number."
        new_vehicle = Bike(vid, name, rent, cc)

    # Add to dictionary and save
    vehicles[vid] = new_vehicle
    save_vehicles(vehicles)
    return True, f"Vehicle '{name}' added successfully!"


def rent_vehicle(vehicle_id, customer_name, contact, days_str):
    """
    Rent a vehicle to a customer.
    Marks vehicle as unavailable and creates a rental record.
    Returns (True, message, bill_info) or (False, error, None).
    """
    vehicles = load_vehicles()
    rentals  = load_rentals()

    # Check if vehicle exists
    if vehicle_id not in vehicles:
        return False, f"No vehicle found with ID '{vehicle_id}'.", None

    vehicle = vehicles[vehicle_id]

    # Check if it's available
    if not vehicle.get_availability():
        return False, f"Vehicle '{vehicle.get_name()}' is currently rented out.", None

    # Validate days
    try:
        days = int(days_str)
        if days <= 0:
            return False, "Number of rental days must be at least 1.", None
    except ValueError:
        return False, "Rental days must be a whole number.", None

    # Calculate bill
    base_bill              = calculate_rental_bill(vehicle.get_rent_per_day(), days)
    final_bill, discount_p = apply_discount(base_bill, days)

    # Create rental record
    rental_id   = generate_rental_id(rentals)
    today_str   = date.today().strftime("%Y-%m-%d")

    rental_record = {
        "rental_id"   : rental_id,
        "vehicle_id"  : vehicle_id,
        "customer"    : customer_name,
        "contact"     : contact,
        "days"        : days,
        "rent_date"   : today_str,
        "return_date" : "ACTIVE",
        "total_bill"  : str(round(final_bill, 2))
    }

    # Mark vehicle as unavailable
    vehicle.set_availability(False)

    # Save everything
    rentals.append(rental_record)
    save_rentals(rentals)
    save_vehicles(vehicles)
    save_customer(customer_name, contact, vehicle_id, today_str)

    bill_info = {
        "rental_id"  : rental_id,
        "base_bill"  : base_bill,
        "discount"   : discount_p,
        "final_bill" : final_bill
    }
    return True, "Vehicle rented successfully!", bill_info


def return_vehicle(vehicle_id, actual_days_str):
    """
    Process the return of a rented vehicle.
    Calculates late fines if returned late.
    Returns (True, message, bill_details) or (False, error, None).
    """
    vehicles = load_vehicles()
    rentals  = load_rentals()

    # Find the active rental for this vehicle
    active_rental = None
    for r in rentals:
        if r["vehicle_id"] == vehicle_id and r["return_date"] == "ACTIVE":
            active_rental = r
            break

    if not active_rental:
        return False, f"No active rental found for vehicle ID '{vehicle_id}'.", None

    if vehicle_id not in vehicles:
        return False, "Vehicle not found in system.", None

    # Validate actual days
    try:
        actual_days = int(actual_days_str)
        if actual_days <= 0:
            return False, "Actual rental days must be at least 1.", None
    except ValueError:
        return False, "Actual days must be a whole number.", None

    vehicle       = vehicles[vehicle_id]
    expected_days = active_rental["days"]
    rent_per_day  = vehicle.get_rent_per_day()

    # Calculate all charges
    base_bill              = calculate_rental_bill(rent_per_day, expected_days)
    final_bill, discount_p = apply_discount(base_bill, expected_days)
    late_fine              = calculate_late_fine(expected_days, actual_days, rent_per_day)
    grand_total            = final_bill + late_fine

    # Update rental record
    return_date = date.today().strftime("%Y-%m-%d")
    active_rental["return_date"] = return_date
    active_rental["total_bill"]  = str(round(grand_total, 2))

    # Mark vehicle as available again
    vehicle.set_availability(True)

    # Save updated data
    save_rentals(rentals)
    save_vehicles(vehicles)

    bill_details = {
        "customer"    : active_rental["customer"],
        "vehicle"     : vehicle.get_name(),
        "expected"    : expected_days,
        "actual"      : actual_days,
        "base_bill"   : base_bill,
        "discount"    : discount_p,
        "rental_bill" : final_bill,
        "late_fine"   : late_fine,
        "grand_total" : grand_total
    }
    return True, "Vehicle returned successfully!", bill_details


def search_vehicle_by_id(vehicle_id):
    """
    Search for a vehicle by its ID.
    Returns the Vehicle object if found, or None.
    """
    vehicles = load_vehicles()
    return vehicles.get(vehicle_id, None)


def get_available_vehicles():
    """Return a list of all vehicles that are currently available."""
    vehicles = load_vehicles()
    return [v for v in vehicles.values() if v.get_availability()]


def count_available_vehicles():
    """Return the count of available vehicles."""
    return len(get_available_vehicles())


# ============================================================
# STEP 9: BUILD THE TKINTER GUI
# We create a main App class that holds the entire interface.
# Each feature has its own "frame" (screen/tab).
# ============================================================

# ----- Color Palette (Charcoal, Gold, Crisp White) -----
BG_DARK    = "#2B2B2B"   # Charcoal - main background
BG_MEDIUM  = "#3A3A3A"   # Slightly lighter charcoal for panels
BG_CARD    = "#333333"   # Card/form background
GOLD       = "#D4A017"   # Gold - accent, buttons, highlights
GOLD_HOVER = "#E8B820"   # Lighter gold for hover
GOLD_DARK  = "#A87C10"   # Darker gold for pressed state
WHITE      = "#F5F5F0"   # Crisp white - text
GRAY_TEXT  = "#AAAAAA"   # Muted gray for secondary text
SUCCESS    = "#4CAF50"   # Green for success messages
ERROR      = "#E53935"   # Red for error messages
DIVIDER    = "#444444"   # Subtle divider lines

# ----- Font Styles -----
FONT_TITLE   = ("Georgia", 20, "bold")
FONT_HEADING = ("Georgia", 14, "bold")
FONT_SUBHEAD = ("Helvetica", 11, "bold")
FONT_BODY    = ("Helvetica", 10)
FONT_LABEL   = ("Helvetica", 10, "bold")
FONT_SMALL   = ("Helvetica", 9)
FONT_BTN     = ("Helvetica", 10, "bold")


class CarRentalApp:
    """
    Main Application Class.
    This class builds and manages the entire GUI window.
    """

    def __init__(self, root):
        """
        Constructor: Set up the main window and build the UI.
        'root' is the Tkinter main window passed from outside.
        """
        self.root = root
        self.setup_main_window()
        self.create_sidebar()
        self.create_content_area()
        self.show_dashboard()   # Show dashboard by default on startup

    # ----------------------------------------------------------
    # MAIN WINDOW SETUP
    # ----------------------------------------------------------

    def setup_main_window(self):
        """Configure the main application window."""
        self.root.title("🚗  Car Rental Management System")
        self.root.configure(bg=BG_DARK)

        # Make window full screen
        self.root.state("zoomed")        # Works on Windows
        self.root.minsize(1100, 650)

        # Allow window to resize with content
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    # ----------------------------------------------------------
    # SIDEBAR (LEFT NAVIGATION PANEL)
    # ----------------------------------------------------------

    def create_sidebar(self):
        """Build the left navigation sidebar with menu buttons."""
        # Sidebar container
        self.sidebar = tk.Frame(self.root, bg=BG_MEDIUM, width=220)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)  # Keep fixed width

        # Logo / App title at top of sidebar
        logo_frame = tk.Frame(self.sidebar, bg=GOLD, pady=18)
        logo_frame.pack(fill="x")

        tk.Label(logo_frame, text="🚗", font=("Helvetica", 26),
                 bg=GOLD, fg=BG_DARK).pack()
        tk.Label(logo_frame, text="CAR RENTAL", font=("Georgia", 12, "bold"),
                 bg=GOLD, fg=BG_DARK).pack()
        tk.Label(logo_frame, text="MANAGEMENT SYSTEM", font=("Helvetica", 7, "bold"),
                 bg=GOLD, fg=BG_DARK).pack(pady=(0, 4))

        # Spacer
        tk.Frame(self.sidebar, bg=BG_MEDIUM, height=15).pack()

        # Navigation menu buttons
        # Each button calls show_XXX() to switch the content area
        nav_items = [
            ("📊  Dashboard",       self.show_dashboard),
            ("➕  Add Vehicle",     self.show_add_vehicle),
            ("🚗  View Vehicles",   self.show_view_vehicles),
            ("🔍  Search Vehicle",  self.show_search_vehicle),
            ("📋  Rent Vehicle",    self.show_rent_vehicle),
            ("↩️  Return Vehicle",  self.show_return_vehicle),
            ("📁  Rental Records",  self.show_records),
        ]

        self.nav_buttons = {}
        for text, command in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg=BG_MEDIUM,
                fg=WHITE,
                font=FONT_BTN,
                anchor="w",
                padx=22,
                pady=10,
                relief="flat",
                cursor="hand2",
                bd=0,
                activebackground=GOLD,
                activeforeground=BG_DARK,
            )
            btn.pack(fill="x", pady=1)

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=GOLD, fg=BG_DARK))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG_MEDIUM, fg=WHITE))

            self.nav_buttons[text] = btn

        # Bottom: availability counter
        tk.Frame(self.sidebar, bg=DIVIDER, height=1).pack(fill="x", pady=15)
        self.avail_label = tk.Label(
            self.sidebar,
            text=self._avail_text(),
            bg=BG_MEDIUM,
            fg=GOLD,
            font=FONT_SMALL,
            justify="center",
            wraplength=180
        )
        self.avail_label.pack(pady=5, padx=10)

    def _avail_text(self):
        """Return formatted availability counter text."""
        count = count_available_vehicles()
        return f"🟢  {count} Vehicle(s) Available"

    def refresh_availability_counter(self):
        """Update the availability counter in the sidebar."""
        self.avail_label.config(text=self._avail_text())

    # ----------------------------------------------------------
    # CONTENT AREA (RIGHT SIDE - changes with each menu click)
    # ----------------------------------------------------------

    def create_content_area(self):
        """Create the main content frame on the right side."""
        self.content_frame = tk.Frame(self.root, bg=BG_DARK)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def clear_content(self):
        """Remove all widgets from the content area (to load new screen)."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def make_scroll_canvas(self):
        """
        Create a scrollable canvas inside content_frame.
        Returns (canvas, scrollable_frame) so we can add widgets to scrollable_frame.
        """
        canvas = tk.Canvas(self.content_frame, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_DARK)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        return canvas, scrollable_frame

    # ----------------------------------------------------------
    # HELPER: Page title header
    # ----------------------------------------------------------

    def make_page_header(self, parent, icon, title, subtitle=""):
        """Create a styled page header with icon, title, and subtitle."""
        header = tk.Frame(parent, bg=BG_DARK, pady=20)
        header.pack(fill="x", padx=30)

        title_row = tk.Frame(header, bg=BG_DARK)
        title_row.pack(anchor="w")

        tk.Label(title_row, text=f"{icon}  {title}", font=FONT_TITLE,
                 bg=BG_DARK, fg=WHITE).pack(side="left")

        if subtitle:
            tk.Label(header, text=subtitle, font=FONT_SMALL,
                     bg=BG_DARK, fg=GRAY_TEXT).pack(anchor="w")

        # Gold underline
        tk.Frame(header, bg=GOLD, height=2).pack(fill="x", pady=(8, 0))

    # ----------------------------------------------------------
    # HELPER: Styled card / form container
    # ----------------------------------------------------------

    def make_card(self, parent, padx=30, pady=15):
        """Create a styled card container for forms and content."""
        outer = tk.Frame(parent, bg=BG_CARD, padx=padx, pady=pady,
                         relief="flat", bd=0)
        return outer

    # ----------------------------------------------------------
    # HELPER: Labeled entry field
    # ----------------------------------------------------------

    def make_field(self, parent, label_text, row, var, width=30, col_offset=0):
        """Create a label + entry field pair in a grid."""
        tk.Label(parent, text=label_text, bg=BG_CARD, fg=GOLD,
                 font=FONT_LABEL, anchor="w").grid(
            row=row, column=col_offset, padx=(10, 8), pady=8, sticky="w")

        entry = tk.Entry(parent, textvariable=var, width=width,
                         bg=BG_MEDIUM, fg=WHITE, font=FONT_BODY,
                         insertbackground=WHITE, relief="flat",
                         highlightthickness=1, highlightcolor=GOLD,
                         highlightbackground=DIVIDER)
        entry.grid(row=row, column=col_offset + 1, padx=(0, 20), pady=8, sticky="ew")
        return entry

    # ----------------------------------------------------------
    # HELPER: Gold action button
    # ----------------------------------------------------------

    def make_btn(self, parent, text, command, width=18):
        """Create a styled gold action button."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=GOLD,
            fg=BG_DARK,
            font=FONT_BTN,
            width=width,
            relief="flat",
            cursor="hand2",
            activebackground=GOLD_HOVER,
            activeforeground=BG_DARK,
            pady=7
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=GOLD_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=GOLD))
        return btn

    # ----------------------------------------------------------
    # HELPER: Result message label
    # ----------------------------------------------------------

    def make_result_label(self, parent):
        """Create a label for showing success/error messages."""
        lbl = tk.Label(parent, text="", bg=BG_CARD, font=FONT_BODY, pady=5)
        return lbl

    def show_msg(self, label, msg, success=True):
        """Display a message in the result label with color coding."""
        label.config(text=msg, fg=SUCCESS if success else ERROR)

    # ==========================================================
    # STEP 10: CONNECT BUTTONS TO FUNCTIONS (SCREENS)
    # Each show_XXX() method builds one "page" of the app.
    # ==========================================================

    # ----------------------------------------------------------
    # DASHBOARD SCREEN
    # ----------------------------------------------------------

    def show_dashboard(self):
        """Show the main dashboard with stats and overview."""
        self.clear_content()
        _, frame = self.make_scroll_canvas()

        self.make_page_header(frame, "📊", "Dashboard",
                              "Welcome to the Car Rental Management System")

        # Load data for stats
        vehicles  = load_vehicles()
        rentals   = load_rentals()
        customers = load_customers()

        total_v  = len(vehicles)
        avail_v  = sum(1 for v in vehicles.values() if v.get_availability())
        rented_v = total_v - avail_v
        active_r = sum(1 for r in rentals if r["return_date"] == "ACTIVE")

        # --- Stats cards row ---
        stats_frame = tk.Frame(frame, bg=BG_DARK)
        stats_frame.pack(fill="x", padx=30, pady=10)
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        stat_data = [
            ("🚗", "Total Vehicles",    str(total_v),  GOLD),
            ("🟢", "Available",         str(avail_v),  SUCCESS),
            ("🔴", "Currently Rented",  str(rented_v), "#E57373"),
            ("📋", "Active Rentals",    str(active_r), "#64B5F6"),
        ]

        for i, (icon, title, value, color) in enumerate(stat_data):
            card = tk.Frame(stats_frame, bg=BG_CARD, padx=20, pady=18, relief="flat")
            card.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            tk.Label(card, text=icon, font=("Helvetica", 26), bg=BG_CARD, fg=color).pack()
            tk.Label(card, text=value, font=("Georgia", 28, "bold"),
                     bg=BG_CARD, fg=color).pack()
            tk.Label(card, text=title, font=FONT_SMALL,
                     bg=BG_CARD, fg=GRAY_TEXT).pack()

        # --- Recent active rentals ---
        tk.Frame(frame, bg=DIVIDER, height=1).pack(fill="x", padx=30, pady=15)
        tk.Label(frame, text="  Active Rentals", font=FONT_HEADING,
                 bg=BG_DARK, fg=GOLD).pack(anchor="w", padx=30)

        tbl_frame = tk.Frame(frame, bg=BG_DARK, padx=30)
        tbl_frame.pack(fill="x", pady=8)

        cols = ("Rental ID", "Vehicle ID", "Customer", "Contact", "Days", "Rent Date")
        tree = ttk.Treeview(tbl_frame, columns=cols, show="headings", height=7)
        self._style_treeview(tree, cols)

        active = [r for r in rentals if r["return_date"] == "ACTIVE"]
        if active:
            for r in active:
                tree.insert("", "end", values=(
                    r["rental_id"], r["vehicle_id"], r["customer"],
                    r["contact"], r["days"], r["rent_date"]))
        else:
            tree.insert("", "end", values=("—", "No active rentals", "—", "—", "—", "—"))

        tree.pack(fill="x")

        # --- Quick guide ---
        tk.Frame(frame, bg=DIVIDER, height=1).pack(fill="x", padx=30, pady=15)
        guide_frame = tk.Frame(frame, bg=BG_CARD, padx=25, pady=15)
        guide_frame.pack(fill="x", padx=30, pady=5)

        tk.Label(guide_frame, text="📌  Quick Guide", font=FONT_HEADING,
                 bg=BG_CARD, fg=GOLD).pack(anchor="w")

        steps = [
            "1. Add Vehicle  →  Register a new car or bike in the system.",
            "2. Rent Vehicle →  Assign a vehicle to a customer for N days.",
            "3. Return Vehicle → Mark return, auto-calculate bill + late fine.",
            "4. View Vehicles  → See all vehicles and their availability.",
            "5. Search Vehicle → Find a specific vehicle by its ID.",
            "6. Rental Records → Browse all past and active rentals.",
        ]
        for s in steps:
            tk.Label(guide_frame, text=s, font=FONT_BODY,
                     bg=BG_CARD, fg=WHITE, anchor="w").pack(anchor="w", pady=2)

        tk.Frame(frame, bg=BG_DARK, height=30).pack()

    # ----------------------------------------------------------
    # ADD VEHICLE SCREEN
    # ----------------------------------------------------------

    def show_add_vehicle(self):
        """Form to add a new Car or Bike to the system."""
        self.clear_content()
        _, frame = self.make_scroll_canvas()

        self.make_page_header(frame, "➕", "Add Vehicle",
                              "Register a new car or bike in the system")

        # Form card
        card = self.make_card(frame)
        card.pack(fill="x", padx=30, pady=10)
        card.columnconfigure(1, weight=1)
        card.columnconfigure(3, weight=1)

        # StringVars hold the form data
        vtype    = tk.StringVar(value="Car")
        vid      = tk.StringVar()
        vname    = tk.StringVar()
        vrent    = tk.StringVar()
        seats    = tk.StringVar()
        fuel     = tk.StringVar(value="Petrol")
        enginecc = tk.StringVar()

        # Vehicle Type selector
        tk.Label(card, text="Vehicle Type:", bg=BG_CARD, fg=GOLD,
                 font=FONT_LABEL).grid(row=0, column=0, padx=10, pady=12, sticky="w")

        type_frame = tk.Frame(card, bg=BG_CARD)
        type_frame.grid(row=0, column=1, sticky="w", padx=(0, 20))

        for vt in ["Car", "Bike"]:
            rb = tk.Radiobutton(type_frame, text=vt, variable=vtype, value=vt,
                                bg=BG_CARD, fg=WHITE, selectcolor=GOLD,
                                activebackground=BG_CARD, font=FONT_BODY,
                                command=self._toggle_extra_fields_ref(vtype, card, seats, fuel, enginecc))
            rb.pack(side="left", padx=10)

        # Common fields
        self.make_field(card, "Vehicle ID:",    1, vid,   30)
        self.make_field(card, "Vehicle Name:",  2, vname, 30)
        self.make_field(card, "Rent Per Day (PKR):", 3, vrent, 30)

        # --- Car-specific fields ---
        self.car_fields_frame = tk.Frame(card, bg=BG_CARD)
        self.car_fields_frame.grid(row=4, column=0, columnspan=4, sticky="ew")

        self.make_field(self.car_fields_frame, "Number of Seats:", 0, seats, 30)

        tk.Label(self.car_fields_frame, text="Fuel Type:", bg=BG_CARD,
                 fg=GOLD, font=FONT_LABEL).grid(row=1, column=0, padx=10, pady=8, sticky="w")

        fuel_combo = ttk.Combobox(self.car_fields_frame, textvariable=fuel, width=28,
                                  values=["Petrol", "Diesel", "Electric", "Hybrid"],
                                  state="readonly", font=FONT_BODY)
        fuel_combo.grid(row=1, column=1, pady=8, sticky="w")

        # --- Bike-specific fields ---
        self.bike_fields_frame = tk.Frame(card, bg=BG_CARD)
        self.bike_fields_frame.grid(row=5, column=0, columnspan=4, sticky="ew")
        self.bike_fields_frame.grid_remove()   # Hidden by default

        self.make_field(self.bike_fields_frame, "Engine CC:", 0, enginecc, 30)

        # Result label
        result_lbl = self.make_result_label(card)
        result_lbl.grid(row=6, column=0, columnspan=4, pady=5)

        # Submit button
        def do_add():
            """Gather form values and call add_vehicle()."""
            t = vtype.get()
            ok, msg = add_vehicle(
                t, vid.get().strip(), vname.get().strip(),
                vrent.get().strip(),
                seats.get().strip() if t == "Car" else enginecc.get().strip(),
                fuel.get() if t == "Car" else ""
            )
            self.show_msg(result_lbl, msg, ok)
            if ok:
                # Clear the form after success
                vid.set(""); vname.set(""); vrent.set("")
                seats.set(""); enginecc.set("")
                self.refresh_availability_counter()

        btn_frame = tk.Frame(card, bg=BG_CARD)
        btn_frame.grid(row=7, column=0, columnspan=4, pady=15)

        self.make_btn(btn_frame, "✅  Add Vehicle", do_add).pack(side="left", padx=10)
        self.make_btn(btn_frame, "🔄  Clear Form",
                      lambda: [v.set("") for v in [vid, vname, vrent, seats, enginecc]]).pack(side="left", padx=10)

        tk.Frame(frame, bg=BG_DARK, height=30).pack()

    def _toggle_extra_fields_ref(self, vtype_var, card, seats, fuel, enginecc):
        """
        Returns a function that shows/hides car or bike fields
        depending on which vehicle type is selected.
        (We return a function so it can be called by the radiobutton command.)
        """
        def toggle():
            if vtype_var.get() == "Car":
                self.car_fields_frame.grid()
                self.bike_fields_frame.grid_remove()
            else:
                self.car_fields_frame.grid_remove()
                self.bike_fields_frame.grid()
        return toggle

    # ----------------------------------------------------------
    # VIEW VEHICLES SCREEN
    # ----------------------------------------------------------

    def show_view_vehicles(self):
        """Show all vehicles in a table with filter options."""
        self.clear_content()
        _, frame = self.make_scroll_canvas()

        self.make_page_header(frame, "🚗", "View Vehicles",
                              "Browse all registered vehicles and their status")

        # Filter row
        filter_frame = tk.Frame(frame, bg=BG_DARK, padx=30)
        filter_frame.pack(fill="x", pady=8)

        tk.Label(filter_frame, text="Filter:", bg=BG_DARK, fg=GOLD,
                 font=FONT_LABEL).pack(side="left", padx=(0, 8))

        filter_var = tk.StringVar(value="All")
        for opt in ["All", "Available Only", "Rented Only", "Cars Only", "Bikes Only"]:
            rb = tk.Radiobutton(filter_frame, text=opt, variable=filter_var, value=opt,
                                bg=BG_DARK, fg=WHITE, selectcolor=GOLD,
                                activebackground=BG_DARK, font=FONT_BODY)
            rb.pack(side="left", padx=6)

        # Table
        tbl_frame = tk.Frame(frame, bg=BG_DARK, padx=30)
        tbl_frame.pack(fill="x", pady=10)

        cols = ("ID", "Type", "Name", "Rent/Day(PKR)", "Seats", "Fuel", "CC", "Status")
        tree = ttk.Treeview(tbl_frame, columns=cols, show="headings", height=16)
        self._style_treeview(tree, cols, col_widths=[70, 60, 160, 110, 60, 70, 60, 90])

        scrollb = ttk.Scrollbar(tbl_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollb.set)
        tree.pack(side="left", fill="x", expand=True)
        scrollb.pack(side="right", fill="y")

        def refresh_table():
            """Re-populate the table based on current filter."""
            tree.delete(*tree.get_children())
            vehicles = load_vehicles()
            filt     = filter_var.get()

            for v in vehicles.values():
                if filt == "Available Only" and not v.get_availability():
                    continue
                if filt == "Rented Only" and v.get_availability():
                    continue
                if filt == "Cars Only" and v.get_type() != "Car":
                    continue
                if filt == "Bikes Only" and v.get_type() != "Bike":
                    continue
                row = v.get_display_info()
                tag = "available" if v.get_availability() else "rented"
                tree.insert("", "end", values=row, tags=(tag,))

            tree.tag_configure("available", foreground="#A5D6A7")
            tree.tag_configure("rented",    foreground="#EF9A9A")

        # Apply filter button
        self.make_btn(filter_frame, "Apply Filter", refresh_table, width=14).pack(side="left", padx=10)

        refresh_table()   # Load table on open

        tk.Frame(frame, bg=BG_DARK, height=30).pack()

    # ----------------------------------------------------------
    # SEARCH VEHICLE SCREEN
    # ----------------------------------------------------------

    def show_search_vehicle(self):
        """Search for a vehicle by its ID."""
        self.clear_content()
        _, frame = self.make_scroll_canvas()

        self.make_page_header(frame, "🔍", "Search Vehicle",
                              "Find a vehicle by entering its unique ID")

        card = self.make_card(frame)
        card.pack(fill="x", padx=30, pady=10)
        card.columnconfigure(1, weight=1)

        sid = tk.StringVar()
        self.make_field(card, "Vehicle ID:", 0, sid, 25)

        result_lbl = self.make_result_label(card)
        result_lbl.grid(row=1, column=0, columnspan=2, pady=5)

        # Result display area
        result_card = tk.Frame(frame, bg=BG_CARD, padx=25, pady=20)

        def do_search():
            result_card.pack_forget()
            vid = sid.get().strip()
            if not vid:
                self.show_msg(result_lbl, "Please enter a Vehicle ID.", False)
                return

            vehicle = search_vehicle_by_id(vid)
            if not vehicle:
                self.show_msg(result_lbl, f"No vehicle found with ID '{vid}'.", False)
                return

            self.show_msg(result_lbl, "Vehicle found!", True)

            # Clear old result
            for w in result_card.winfo_children():
                w.destroy()

            result_card.pack(fill="x", padx=30, pady=5)
            tk.Label(result_card, text="🔍  Search Result",
                     font=FONT_HEADING, bg=BG_CARD, fg=GOLD).pack(anchor="w", pady=(0, 10))

            info = vehicle.get_display_info()  # [ID, Type, Name, Rent, ...]
            avail_text  = "✅ Available" if vehicle.get_availability() else "❌ Currently Rented"
            avail_color = SUCCESS if vehicle.get_availability() else ERROR

            fields_info = [
                ("Vehicle ID",    vehicle.get_id()),
                ("Type",          vehicle.get_type()),
                ("Name",          vehicle.get_name()),
                ("Rent Per Day",  f"PKR {vehicle.get_rent_per_day():,.0f}"),
                ("Availability",  avail_text),
            ]

            if vehicle.get_type() == "Car":
                fields_info += [("Seats",     str(vehicle.get_seats())),
                                ("Fuel Type", vehicle.get_fuel_type())]
            else:
                fields_info += [("Engine CC", f"{vehicle.get_engine_cc()} CC")]

            for lbl, val in fields_info:
                row = tk.Frame(result_card, bg=BG_CARD)
                row.pack(fill="x", pady=3)
                tk.Label(row, text=f"{lbl}:", width=16, anchor="w",
                         font=FONT_LABEL, bg=BG_CARD, fg=GOLD).pack(side="left")
                color = avail_color if lbl == "Availability" else WHITE
                tk.Label(row, text=val, font=FONT_BODY,
                         bg=BG_CARD, fg=color).pack(side="left")

        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.grid(row=2, column=0, columnspan=2, pady=12)
        self.make_btn(btn_row, "🔍  Search", do_search).pack()

        tk.Frame(frame, bg=BG_DARK, height=30).pack()
    # ----------------------------------------------------------
    # RENT VEHICLE SCREEN
    # ----------------------------------------------------------
    def show_rent_vehicle(self):
        """Form to rent a vehicle to a customer."""
        self.clear_content()
        _, frame = self.make_scroll_canvas()
        self.make_page_header(frame, "📋", "Rent Vehicle",
                              "Assign an available vehicle to a customer")
        card = self.make_card(frame)
        card.pack(fill="x", padx=30, pady=10)
        card.columnconfigure(1, weight=1)
        vid      = tk.StringVar()
        cname    = tk.StringVar()
        ccontact = tk.StringVar()
        days     = tk.StringVar()
        self.make_field(card, "Vehicle ID:",     0, vid,      25)
        self.make_field(card, "Customer Name:",  1, cname,    25)
        self.make_field(card, "Contact No.:",    2, ccontact, 25)
        self.make_field(card, "Rental Days:",    3, days,     25)
        result_lbl = self.make_result_label(card)
        result_lbl.grid(row=4, column=0, columnspan=2, pady=5)
        # Bill display
        bill_card = tk.Frame(frame, bg=BG_CARD, padx=25, pady=15)
        def do_rent():
            bill_card.pack_forget()
            ok, msg, bill_info = rent_vehicle(
                vid.get().strip(), cname.get().strip(),
                ccontact.get().strip(), days.get().strip()
            )
            self.show_msg(result_lbl, msg, ok)

            if ok and bill_info:
                # Show billing summary
                for w in bill_card.winfo_children():
                    w.destroy()
                bill_card.pack(fill="x", padx=30, pady=5)

                tk.Label(bill_card, text="💰  Billing Summary",
                         font=FONT_HEADING, bg=BG_CARD, fg=GOLD).pack(anchor="w", pady=(0, 8))

                bill_rows = [
                    ("Rental ID",       bill_info["rental_id"]),
                    ("Base Bill",       f"PKR {bill_info['base_bill']:,.2f}"),
                    ("Discount",        f"{bill_info['discount']:.0f}%"),
                    ("Final Bill",      f"PKR {bill_info['final_bill']:,.2f}"),
                ]
                for lbl, val in bill_rows:
                    r = tk.Frame(bill_card, bg=BG_CARD)
                    r.pack(fill="x", pady=2)
                    tk.Label(r, text=f"{lbl}:", width=16, anchor="w",
                             font=FONT_LABEL, bg=BG_CARD, fg=GOLD).pack(side="left")
                    color = SUCCESS if lbl == "Final Bill" else WHITE
                    tk.Label(r, text=val, font=FONT_BODY, bg=BG_CARD, fg=color).pack(side="left")

                # Clear form
                for v in [vid, cname, ccontact, days]:
                    v.set("")
                self.refresh_availability_counter()

        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.grid(row=5, column=0, columnspan=2, pady=12)
        self.make_btn(btn_row, "📋  Rent Vehicle", do_rent, 18).pack(side="left", padx=8)
        self.make_btn(btn_row, "🔄  Clear",
                      lambda: [v.set("") for v in [vid, cname, ccontact, days]], 12).pack(side="left", padx=8)

        tk.Frame(frame, bg=BG_DARK, height=30).pack()

    # ----------------------------------------------------------
    # RETURN VEHICLE SCREEN
    # ----------------------------------------------------------

    def show_return_vehicle(self):
        """Form to return a rented vehicle and calculate final bill."""
        self.clear_content()
        _, frame = self.make_scroll_canvas()

        self.make_page_header(frame, "↩️", "Return Vehicle",
                              "Process a vehicle return and calculate the final bill")

        card = self.make_card(frame)
        card.pack(fill="x", padx=30, pady=10)
        card.columnconfigure(1, weight=1)

        vid         = tk.StringVar()
        actual_days = tk.StringVar()

        self.make_field(card, "Vehicle ID:",     0, vid,         25)
        self.make_field(card, "Actual Days Used:", 1, actual_days, 25)

        tk.Label(card, text="  (Enter how many days the vehicle was actually used)",
                 bg=BG_CARD, fg=GRAY_TEXT, font=FONT_SMALL).grid(
            row=2, column=1, sticky="w", padx=5)

        result_lbl = self.make_result_label(card)
        result_lbl.grid(row=3, column=0, columnspan=2, pady=5)

        # Bill display
        bill_card = tk.Frame(frame, bg=BG_CARD, padx=25, pady=15)

        def do_return():
            bill_card.pack_forget()
            ok, msg, bill_details = return_vehicle(
                vid.get().strip(), actual_days.get().strip()
            )
            self.show_msg(result_lbl, msg, ok)

            if ok and bill_details:
                for w in bill_card.winfo_children():
                    w.destroy()
                bill_card.pack(fill="x", padx=30, pady=5)

                tk.Label(bill_card, text="🧾  Final Bill",
                         font=FONT_HEADING, bg=BG_CARD, fg=GOLD).pack(anchor="w", pady=(0, 8))

                rows = [
                    ("Customer",       bill_details["customer"]),
                    ("Vehicle",        bill_details["vehicle"]),
                    ("Expected Days",  str(bill_details["expected"])),
                    ("Actual Days",    str(bill_details["actual"])),
                    ("Base Bill",      f"PKR {bill_details['base_bill']:,.2f}"),
                    ("Discount",       f"{bill_details['discount']:.0f}%"),
                    ("Rental Bill",    f"PKR {bill_details['rental_bill']:,.2f}"),
                    ("Late Fine",      f"PKR {bill_details['late_fine']:,.2f}"),
                    ("GRAND TOTAL",    f"PKR {bill_details['grand_total']:,.2f}"),
                ]

                for lbl, val in rows:
                    r = tk.Frame(bill_card, bg=BG_CARD)
                    r.pack(fill="x", pady=2)
                    is_total = lbl == "GRAND TOTAL"
                    is_fine  = lbl == "Late Fine" and bill_details["late_fine"] > 0

                    lbl_color = GOLD if is_total else (ERROR if is_fine else GOLD)
                    val_color = SUCCESS if is_total else (ERROR if is_fine else WHITE)
                    fnt = FONT_HEADING if is_total else FONT_BODY

                    tk.Label(r, text=f"{lbl}:", width=16, anchor="w",
                             font=FONT_LABEL if not is_total else ("Helvetica", 11, "bold"),
                             bg=BG_CARD, fg=lbl_color).pack(side="left")
                    tk.Label(r, text=val, font=fnt,
                             bg=BG_CARD, fg=val_color).pack(side="left")

                    if is_total:
                        tk.Frame(bill_card, bg=GOLD, height=1).pack(fill="x", pady=(4, 0))

                for v in [vid, actual_days]:
                    v.set("")
                self.refresh_availability_counter()

        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.grid(row=4, column=0, columnspan=2, pady=12)
        self.make_btn(btn_row, "↩️  Process Return", do_return, 18).pack(side="left", padx=8)
        self.make_btn(btn_row, "🔄  Clear",
                      lambda: [v.set("") for v in [vid, actual_days]], 12).pack(side="left", padx=8)

        tk.Frame(frame, bg=BG_DARK, height=30).pack()

    # ----------------------------------------------------------
    # RENTAL RECORDS SCREEN
    # ----------------------------------------------------------

    def show_records(self):
        """Show all rental history records."""
        self.clear_content()
        _, frame = self.make_scroll_canvas()

        self.make_page_header(frame, "📁", "Rental Records",
                              "Complete history of all vehicle rentals")

        # Filter row
        filter_frame = tk.Frame(frame, bg=BG_DARK, padx=30)
        filter_frame.pack(fill="x", pady=8)

        filter_var = tk.StringVar(value="All")
        tk.Label(filter_frame, text="Show:", bg=BG_DARK, fg=GOLD,
                 font=FONT_LABEL).pack(side="left", padx=(0, 8))

        for opt in ["All", "Active Only", "Completed Only"]:
            tk.Radiobutton(filter_frame, text=opt, variable=filter_var, value=opt,
                           bg=BG_DARK, fg=WHITE, selectcolor=GOLD,
                           activebackground=BG_DARK, font=FONT_BODY).pack(side="left", padx=6)

        # Table
        tbl_frame = tk.Frame(frame, bg=BG_DARK, padx=30)
        tbl_frame.pack(fill="both", expand=True, pady=10)

        cols = ("Rental ID", "Vehicle ID", "Customer", "Contact",
                "Days", "Rent Date", "Return Date", "Total Bill (PKR)")

        tree = ttk.Treeview(tbl_frame, columns=cols, show="headings", height=18)
        self._style_treeview(tree, cols, col_widths=[70, 80, 140, 110, 50, 100, 100, 120])

        scrollb = ttk.Scrollbar(tbl_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollb.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollb.pack(side="right", fill="y")

        def refresh():
            tree.delete(*tree.get_children())
            rentals = load_rentals()
            filt    = filter_var.get()
            for r in rentals:
                if filt == "Active Only"    and r["return_date"] != "ACTIVE":
                    continue
                if filt == "Completed Only" and r["return_date"] == "ACTIVE":
                    continue
                tag = "active" if r["return_date"] == "ACTIVE" else "done"
                tree.insert("", "end", values=(
                    r["rental_id"], r["vehicle_id"], r["customer"],
                    r["contact"], r["days"], r["rent_date"],
                    r["return_date"], f"PKR {float(r['total_bill']):,.2f}"
                ), tags=(tag,))

            tree.tag_configure("active", foreground="#FFD54F")
            tree.tag_configure("done",   foreground="#A5D6A7")

        self.make_btn(filter_frame, "Apply Filter", refresh, 14).pack(side="left", padx=10)
        refresh()

        # Customer records section
        tk.Frame(frame, bg=DIVIDER, height=1).pack(fill="x", padx=30, pady=15)
        tk.Label(frame, text="  Customer Records", font=FONT_HEADING,
                 bg=BG_DARK, fg=GOLD).pack(anchor="w", padx=30)

        cust_frame = tk.Frame(frame, bg=BG_DARK, padx=30)
        cust_frame.pack(fill="x", pady=8)

        ccols = ("Customer Name", "Contact", "Vehicle Rented", "Rent Date")
        ctree = ttk.Treeview(cust_frame, columns=ccols, show="headings", height=8)
        self._style_treeview(ctree, ccols, col_widths=[160, 120, 110, 110])

        customers = load_customers()
        for c in customers:
            ctree.insert("", "end", values=(c["name"], c["contact"],
                                            c["vehicle_id"], c["rent_date"]))
        ctree.pack(fill="x")

        tk.Frame(frame, bg=BG_DARK, height=30).pack()

    # HELPER: Style the Treeview (table) widget

    def _style_treeview(self, tree, cols, col_widths=None):
        """
        Apply consistent styling to a Treeview widget.
        Sets column headers, widths, fonts, and row colors.
        """
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                         background=BG_CARD,
                         foreground=WHITE,
                         fieldbackground=BG_CARD,
                         rowheight=26,
                         font=FONT_BODY)

        style.configure("Treeview.Heading",
                         background=GOLD,
                         foreground=BG_DARK,
                         font=FONT_SUBHEAD,
                         relief="flat")

        style.map("Treeview",
                  background=[("selected", GOLD_DARK)],
                  foreground=[("selected", WHITE)])

        for i, col in enumerate(cols):
            tree.heading(col, text=col)
            width = col_widths[i] if col_widths and i < len(col_widths) else 100
            tree.column(col, width=width, anchor="center")


# STEP 11: RUN THE MAIN PROGRAM
def main():
    """
    Main entry point of the program.
    Creates the Tkinter window and starts the application.
    """
    root = tk.Tk()

    # Apply global styles
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Vertical.TScrollbar",
                    background=GOLD,
                    troughcolor=BG_MEDIUM,
                    arrowcolor=BG_DARK)

    # Launch the application
    app = CarRentalApp(root)

    # Start the event loop (keeps window open and responsive)
    root.mainloop()


# Python convention: only run main() if this file is run directly
# (not if it's imported by another file)
if __name__ == "__main__":
    main()