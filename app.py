import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
from PIL import Image
from datetime import datetime, date, timedelta
import tkinter as tk

# Set theme and color scheme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Global variables
main_content = None
user_id = None
username = None
is_admin = None

def connect_mysql():
    try:
        connect = mysql.connector.connect(
            host='localhost', user='root',
            password='Prithivi#37', database='bus_sewa'
        )
        return connect
    except mysql.connector.Error as err:
        print("Error:", err)
        return None

def create_login_page():
    # Main window setup
    root = ctk.CTk()
    root.title("BUS SEWA")
    root.geometry("1000x600")
    root.minsize(1040, 640)

    # Create container and frames
    container = ctk.CTkFrame(root, fg_color="transparent")
    container.pack(expand=True, fill="both")

    main_frame = ctk.CTkFrame(container, fg_color="white", width=1000, height=600)
    main_frame.pack(expand=True, padx=20, pady=20)
    main_frame.pack_propagate(False)

    image_frame = ctk.CTkFrame(main_frame, fg_color="white")
    image_frame.pack(side="left", padx=40, pady=40)

    # Load and display images
    login_image = Image.open("bus.jpg")
    login_image = login_image.resize((500, 400))
    login_photo = ctk.CTkImage(light_image=login_image, dark_image=login_image, size=(500, 400))

    signup_image = Image.open("signup.jpg")
    signup_image = signup_image.resize((500, 400))
    signup_photo = ctk.CTkImage(light_image=signup_image, dark_image=signup_image, size=(500, 400))

    login_image_label = ctk.CTkLabel(image_frame, image=login_photo, text="", fg_color="white")
    signup_image_label = ctk.CTkLabel(image_frame, image=signup_photo, text="", fg_color="white")
    login_image_label.pack()

    # Login frame
    login_frame = ctk.CTkFrame(main_frame)
    login_frame.pack(side="right", padx=40, pady=40, fill="both", expand=True)

    # Create signup frame but don't pack it yet
    signup_frame = ctk.CTkFrame(main_frame)

    # Create a scrollable frame inside signup frame
    signup_scroll = ctk.CTkScrollableFrame(signup_frame, width=300, height=500)
    signup_scroll.pack(expand=True, fill="both", padx=20, pady=20)

    def switch_to_login():
        signup_frame.pack_forget()
        signup_image_label.pack_forget()
        image_frame.pack(side="left", padx=40, pady=40)
        login_image_label.pack()
        login_frame.pack(side="right", padx=40, pady=40, fill="both", expand=True)

    def switch_to_signup():
        login_frame.pack_forget()
        login_image_label.pack_forget()
        image_frame.pack(side="right", padx=40, pady=40)
        signup_image_label.pack()
        signup_frame.pack(side="left", padx=40, pady=40, fill="both", expand=True)

    def signin():
        username = username_entry.get()
        password = password_entry.get()
        connect = connect_mysql()
        if connect:
            cursor = connect.cursor()
            query = "SELECT user_id, username, is_admin FROM users WHERE username = %s AND password = %s AND is_active = TRUE"
            cursor.execute(query, (username, password))
            user_data = cursor.fetchone()
            if user_data:
                user_id, username, is_admin = user_data
                messagebox.showinfo("Login Success", f"Welcome {username}!")
                root.destroy()
                open_dashboard(user_id, username, is_admin)
            else:
                messagebox.showerror("Invalid", "Invalid Username or Password")
            cursor.close()
            connect.close()
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")

    def signup():
        username = enter_username.get()
        full_name = enter_fullname.get()
        email = enter_email.get()
        phone = enter_phone.get()
        password = enter_password.get()
        confirm_password = enter_confirm.get()
        
        # Basic validation
        if not all([username, full_name, password, confirm_password]):
            messagebox.showerror('Error', 'Username, Full Name, and Password are required!')
            return
        
        if password != confirm_password:
            messagebox.showerror('Invalid', 'Passwords do not match!')
            return
        
        connect = connect_mysql()
        if connect:
            cursor = connect.cursor()
            try:
                query = """INSERT INTO users 
                          (username, password, full_name, email, phone) 
                          VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (username, password, full_name, email, phone))
                connect.commit()
                messagebox.showinfo('Sign Up', 'Registration Successful!')
                switch_to_login()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
            finally:
                cursor.close()
                connect.close()
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")

    # Login page elements
    header = ctk.CTkLabel(login_frame, text="LOGIN", font=ctk.CTkFont(size=30, weight="bold"))
    header.pack(pady=20)

    username_entry = ctk.CTkEntry(login_frame, 
                                placeholder_text="Username",
                                width=300,
                                height=40,
                                font=ctk.CTkFont(size=14))
    username_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(login_frame, 
                                placeholder_text="Password",
                                width=300,
                                height=40,
                                show="*",
                                font=ctk.CTkFont(size=14))
    password_entry.pack(pady=10)

    login_button = ctk.CTkButton(login_frame, 
                               text="LOGIN",
                               width=200,
                               height=40,
                               font=ctk.CTkFont(size=15),
                               command=signin)
    login_button.pack(pady=20)

    signup_label = ctk.CTkLabel(login_frame, 
                              text="Don't have an account?",
                              font=ctk.CTkFont(size=14))
    signup_label.pack()

    signup_button = ctk.CTkButton(login_frame,
                                text="SIGN UP",
                                width=200,
                                height=40,
                                font=ctk.CTkFont(size=15),
                                command=switch_to_signup)
    signup_button.pack(pady=10)

    # Signup page elements
    header = ctk.CTkLabel(signup_scroll, text="SIGN UP", font=ctk.CTkFont(size=30, weight="bold"))
    header.pack(pady=20)

    enter_username = ctk.CTkEntry(signup_scroll,
                        width=300,
                        height=40,
                        placeholder_text="Username",
                        font=ctk.CTkFont(size=14))
    enter_username.pack(pady=10)
    
    enter_fullname = ctk.CTkEntry(signup_scroll,
                        width=300,
                        height=40,
                        placeholder_text="Full Name",
                        font=ctk.CTkFont(size=14))
    enter_fullname.pack(pady=10)
    
    enter_email = ctk.CTkEntry(signup_scroll,
                        width=300,
                        height=40,
                        placeholder_text="Email",
                        font=ctk.CTkFont(size=14))
    enter_email.pack(pady=10)
    
    enter_phone = ctk.CTkEntry(signup_scroll,
                        width=300,
                        height=40,
                        placeholder_text="Phone",
                        font=ctk.CTkFont(size=14))
    enter_phone.pack(pady=10)

    enter_password = ctk.CTkEntry(signup_scroll,
                         width=300,
                         height=40,
                         placeholder_text="Password",
                         show="*",
                         font=ctk.CTkFont(size=14))
    enter_password.pack(pady=10)

    enter_confirm = ctk.CTkEntry(signup_scroll,
                         width=300,
                         height=40,
                         placeholder_text="Confirm Password",
                         show="*",
                         font=ctk.CTkFont(size=14))
    enter_confirm.pack(pady=10)

    signup_btn = ctk.CTkButton(signup_scroll,
                              text="SIGN UP",
                              width=200,
                              height=40,
                              font=ctk.CTkFont(size=15),
                              command=signup)
    signup_btn.pack(pady=20)

    login_label = ctk.CTkLabel(signup_scroll,
                              text="Already have an account?",
                              font=ctk.CTkFont(size=14))
    login_label.pack()

    login_btn = ctk.CTkButton(signup_scroll,
                             text="LOGIN",
                             width=200,
                             height=40,
                             font=ctk.CTkFont(size=15),
                             command=switch_to_login)
    login_btn.pack(pady=10)

    return root

def open_dashboard(user_id, username, is_admin):
    global main_content  # Add this line to make main_content global
    
    screen = ctk.CTk()
    screen.title("BUS SEWA")
    screen.geometry('1100x700')
    
    # Create sidebar for navigation
    sidebar = ctk.CTkFrame(screen, width=200)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)
    
    # Add logo or app name to sidebar
    app_label = ctk.CTkLabel(sidebar, 
                            text="BUS SEWA",
                            font=ctk.CTkFont(size=20, weight="bold"))
    app_label.pack(pady=20)
    
    # Main content area
    main_content = ctk.CTkFrame(screen)
    main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
    def create_nav_button(text, command):
        return ctk.CTkButton(sidebar,
                           text=text,
                           width=180,
                           height=40,
                           font=ctk.CTkFont(size=14),
                           command=command)
    
    def logout():
        screen.destroy()
        root = create_login_page()
        root.mainloop()

    def search_buses():
        # Clear main content
        for widget in main_content.winfo_children():
            widget.destroy()
            
        # Create a container frame for content
        content_container = ctk.CTkFrame(main_content, fg_color="transparent")
        content_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome header with nice styling
        welcome_frame = ctk.CTkFrame(content_container, fg_color="transparent")
        welcome_frame.pack(fill="x", pady=(20, 30))
        
        welcome_text = ctk.CTkLabel(welcome_frame, 
                                   text=f"Welcome, {username}!", 
                                   font=ctk.CTkFont(size=32, weight="bold"),
                                   text_color="#1F6AA5")
        welcome_text.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(welcome_frame,
                               text="Find your perfect journey",
                               font=ctk.CTkFont(size=16),
                               text_color="gray")
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Search form
        search_frame = ctk.CTkFrame(content_container)
        search_frame.pack(pady=20, fill="x")
        
        # Source city dropdown
        source_label = ctk.CTkLabel(search_frame, text="From:")
        source_label.pack(side="left", padx=10)
        source_var = ctk.StringVar()
        source_dropdown = ctk.CTkComboBox(search_frame, width=150, variable=source_var)
        source_dropdown.pack(side="left", padx=10)

        # Destination city dropdown
        dest_label = ctk.CTkLabel(search_frame, text="To:")
        dest_label.pack(side="left", padx=10)
        dest_var = ctk.StringVar()
        dest_dropdown = ctk.CTkComboBox(search_frame, width=150, variable=dest_var)
        dest_dropdown.pack(side="left", padx=10)

        # Date selection
        date_label = ctk.CTkLabel(search_frame, text="Date:")
        date_label.pack(side="left", padx=10)
        
        # Date options
        date_var = ctk.StringVar()
        today = date.today()
        tomorrow = today + timedelta(days=1)
        date_options = [
            f"Today ({today.strftime('%Y-%m-%d')})",
            f"Tomorrow ({tomorrow.strftime('%Y-%m-%d')})"
        ]
        date_dropdown = ctk.CTkComboBox(search_frame, 
                                       values=date_options,
                                       width=200,
                                       variable=date_var)
        date_dropdown.pack(side="left", padx=10)
        date_dropdown.set(date_options[0])
        
        # Add function to load cities
        def load_cities():
            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    # Get unique source cities
                    cursor.execute("""
                        SELECT DISTINCT source_city 
                        FROM routes 
                        WHERE is_active = TRUE 
                        ORDER BY source_city
                    """)
                    source_cities = [city[0] for city in cursor.fetchall()]
                    source_dropdown.configure(values=source_cities)
                    if source_cities:
                        source_dropdown.set(source_cities[0])

                    # Get unique destination cities
                    cursor.execute("""
                        SELECT DISTINCT destination_city 
                        FROM routes 
                        WHERE is_active = TRUE 
                        ORDER BY destination_city
                    """)
                    dest_cities = [city[0] for city in cursor.fetchall()]
                    dest_dropdown.configure(values=dest_cities)
                    if dest_cities:
                        dest_dropdown.set(dest_cities[0])

                except Exception as e:
                    print(f"Error loading cities: {e}")
                finally:
                    cursor.close()
                    connect.close()

        # Load cities when opening the search page
        load_cities()

        def search():
            display_buses(
                source_dropdown.get(),
                dest_dropdown.get(),
                today if "Today" in date_var.get() else tomorrow
            )
        
        # Search button
        search_btn = ctk.CTkButton(search_frame, 
                                  text="Search",
                                  width=120,
                                  height=32,
                                  font=ctk.CTkFont(size=14),
                                  command=search)
        search_btn.pack(side="left", padx=20)

        # Available Buses Section
        available_frame = ctk.CTkFrame(content_container)
        available_frame.pack(pady=(30, 0), fill="both", expand=True)

        # Header for available buses
        available_label = ctk.CTkLabel(available_frame,
                                     text="Available Buses",
                                     font=ctk.CTkFont(size=20, weight="bold"))
        available_label.pack(pady=(20, 10), padx=20, anchor="w")

        # Create scrollable frame for bus listings
        bus_list_frame = ctk.CTkScrollableFrame(available_frame, height=400)
        bus_list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        def display_buses(source=None, destination=None, travel_date=None):
            # Clear existing bus listings
            for widget in bus_list_frame.winfo_children():
                widget.destroy()

            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    # Updated query to get more route information
                    query = """
                        SELECT 
                            r.route_id,
                            s.schedule_id,
                            b.bus_number,
                            r.source_city,
                            r.destination_city,
                            s.departure_date,
                            s.departure_time,
                            s.available_seats,
                            r.fare,
                            b.bus_name,
                            b.bus_type
                        FROM buses b
                        JOIN schedules s ON b.bus_id = s.bus_id
                        JOIN routes r ON s.route_id = r.route_id
                        WHERE s.departure_date >= %s
                        AND s.departure_date <= %s
                        AND s.available_seats > 0
                        AND b.is_active = TRUE
                        AND r.is_active = TRUE
                        AND s.is_active = TRUE
                    """
                    params = [today, tomorrow]

                    if source and destination:
                        query += " AND r.source_city = %s AND r.destination_city = %s"
                        params.extend([source, destination])

                    if travel_date:
                        query += " AND s.departure_date = %s"
                        params.append(travel_date)

                    query += " ORDER BY s.departure_date, s.departure_time"
                    
                    cursor.execute(query, params)
                    buses = cursor.fetchall()

                    if buses:
                        for bus in buses:
                            # Create frame for each bus
                            bus_frame = ctk.CTkFrame(bus_list_frame)
                            bus_frame.pack(fill="x", padx=10, pady=5)

                            # Bus info header
                            header_frame = ctk.CTkFrame(bus_frame, fg_color="transparent")
                            header_frame.pack(fill="x", padx=15, pady=(10, 5))

                            route_info = ctk.CTkLabel(
                                header_frame,
                                text=f"{bus[9]} ({bus[10]}) - {bus[2]}",
                                font=ctk.CTkFont(size=16, weight="bold")
                            )
                            route_info.pack(side="left")

                            # Main content
                            content_frame = ctk.CTkFrame(bus_frame, fg_color="transparent")
                            content_frame.pack(fill="x", padx=15, pady=5)

                            # Left side info
                            info_left = ctk.CTkFrame(content_frame, fg_color="transparent")
                            info_left.pack(side="left", fill="both", expand=True)

                            # Route with arrow
                            route_label = ctk.CTkLabel(
                                info_left,
                                text=f"{bus[3]} → {bus[4]}",
                                font=ctk.CTkFont(size=14)
                            )
                            route_label.pack(anchor="w", pady=2)

                            # Format time to 12-hour
                            time_obj = datetime.strptime(str(bus[6]), '%H:%M:%S')
                            formatted_time = time_obj.strftime('%I:%M %p')

                            # Date and time
                            schedule_label = ctk.CTkLabel(
                                info_left,
                                text=f"🗓 {bus[5].strftime('%Y-%m-%d')} | ⏰ {formatted_time}",
                                font=ctk.CTkFont(size=14)
                            )
                            schedule_label.pack(anchor="w", pady=2)

                            # Right side info
                            info_right = ctk.CTkFrame(content_frame, fg_color="transparent")
                            info_right.pack(side="right", padx=15)

                            # Fare
                            fare_label = ctk.CTkLabel(
                                info_right,
                                text=f"₹ {bus[8]}",
                                font=ctk.CTkFont(size=16, weight="bold")
                            )
                            fare_label.pack(side="top")

                            # Available seats
                            seats_label = ctk.CTkLabel(
                                info_right,
                                text=f"🪑 {bus[7]} seats available",
                                font=ctk.CTkFont(size=14)
                            )
                            seats_label.pack(side="top", pady=5)

                            def book_now(route_id, schedule_id, source, destination, date, time, fare, bus_number):
                                if messagebox.askyesno("Confirm Booking", 
                                                      f"Do you want to book a ticket for:\n\n"
                                                      f"From: {source}\n"
                                                      f"To: {destination}\n"
                                                      f"Date: {date}\n"
                                                      f"Time: {time}\n"
                                                      f"Bus: {bus_number}\n"
                                                      f"Fare: Rs. {fare}"):
                                    
                                    connect = connect_mysql()
                                    if connect:
                                        cursor = connect.cursor()
                                        try:
                                            # Start transaction
                                            connect.start_transaction()
                                            
                                            # Get user's full name
                                            cursor.execute("""
                                                SELECT full_name FROM users WHERE user_id = %s
                                            """, (user_id,))
                                            passenger_name = cursor.fetchone()[0]
                                            
                                            # Check seat availability
                                            cursor.execute("""
                                                SELECT available_seats 
                                                FROM schedules 
                                                WHERE schedule_id = %s AND is_active = TRUE
                                            """, (schedule_id,))
                                            available_seats = cursor.fetchone()[0]
                                            
                                            if available_seats <= 0:
                                                messagebox.showerror("Error", "Sorry, this bus is now fully booked!")
                                                return
                                            
                                            # Create booking with passenger name and number of seats
                                            cursor.execute("""
                                                INSERT INTO bookings (
                                                    user_id, schedule_id, booking_date, passenger_name, number_of_seats
                                                ) VALUES (%s, %s, CURDATE(), %s, %s)
                                            """, (user_id, schedule_id, passenger_name, 1))  # Setting number_of_seats to 1
                                            
                                            # Update available seats
                                            cursor.execute("""
                                                UPDATE schedules 
                                                SET available_seats = available_seats - 1 
                                                WHERE schedule_id = %s
                                            """, (schedule_id,))
                                            
                                            connect.commit()
                                            
                                            # Show booking confirmation
                                            booking_id = cursor.lastrowid
                                            messagebox.showinfo("Success", 
                                                            f"Booking Confirmed!\n\n"
                                                            f"Booking ID: {booking_id}\n"
                                                            f"Passenger: {passenger_name}\n"
                                                            f"From: {source}\n"
                                                            f"To: {destination}\n"
                                                            f"Date: {date}\n"
                                                            f"Time: {time}\n"
                                                            f"Bus: {bus_number}\n"
                                                            f"Number of Seats: 1\n"
                                                            f"Fare: Rs. {fare}")
                                            
                                            # Refresh the bus listings
                                            display_buses(source_dropdown.get(), 
                                                        dest_dropdown.get(),
                                                        today if "Today" in date_var.get() else tomorrow)
                                            
                                        except Exception as e:
                                            connect.rollback()
                                            messagebox.showerror("Error", f"Failed to book ticket: {str(e)}")
                                        finally:
                                            cursor.close()
                                            connect.close()

                            # Book button
                            book_btn = ctk.CTkButton(
                                info_right,
                                text="Book Now",
                                width=120,
                                height=32,
                                font=ctk.CTkFont(size=14),
                                command=lambda: book_now(
                                    bus[0],  # route_id
                                    bus[1],  # schedule_id
                                    bus[3],  # source
                                    bus[4],  # destination
                                    bus[5],  # date
                                    formatted_time,  # time
                                    bus[8],  # fare
                                    bus[2]   # bus_number
                                )
                            )
                            book_btn.pack(side="top", pady=5)

                    else:
                        no_buses_frame = ctk.CTkFrame(bus_list_frame, fg_color="transparent")
                        no_buses_frame.pack(pady=50)
                        
                        no_buses_label = ctk.CTkLabel(
                            no_buses_frame,
                            text="🚫 No buses available for the selected criteria.",
                            font=ctk.CTkFont(size=16)
                        )
                        no_buses_label.pack()
                        
                        suggestion_label = ctk.CTkLabel(
                            no_buses_frame,
                            text="Try different dates or routes",
                            font=ctk.CTkFont(size=14),
                            text_color="gray"
                        )
                        suggestion_label.pack()

                except Exception as e:
                    print(f"Error fetching buses: {e}")
                    error_frame = ctk.CTkFrame(bus_list_frame, fg_color="transparent")
                    error_frame.pack(pady=50)
                    
                    error_label = ctk.CTkLabel(
                        error_frame,
                        text="⚠️ Error loading bus information.",
                        font=ctk.CTkFont(size=16)
                    )
                    error_label.pack()
                finally:
                    cursor.close()
                    connect.close()

        # Display all available buses by default
        display_buses()

    def book_ticket(route_id, schedule_id, source, destination, departure_date, departure_time, fare, bus_number):
        if messagebox.askyesno("Confirm Booking", 
                              f"Do you want to book a ticket for:\n\n"
                              f"From: {source}\n"
                              f"To: {destination}\n"
                              f"Date: {departure_date}\n"
                              f"Time: {departure_time}\n"
                              f"Bus: {bus_number}\n"
                              f"Fare: Rs. {fare}"):
            
            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    # Start transaction
                    connect.start_transaction()
                    
                    # Check seat availability
                    cursor.execute("""
                        SELECT available_seats 
                        FROM schedules 
                        WHERE schedule_id = %s AND is_active = TRUE
                    """, (schedule_id,))
                    available_seats = cursor.fetchone()[0]
                    
                    if available_seats <= 0:
                        messagebox.showerror("Error", "Sorry, this bus is now fully booked!")
                        return
                    
                    # Create booking - using user_id instead of username
                    cursor.execute("""
                        INSERT INTO bookings (
                            user_id, route_id, schedule_id, booking_date
                        ) VALUES (%s, %s, %s, CURDATE())
                    """, (user_id, route_id, schedule_id))  # user_id variable contains user_id
                    
                    # Update available seats
                    cursor.execute("""
                        UPDATE schedules 
                        SET available_seats = available_seats - 1 
                        WHERE schedule_id = %s
                    """, (schedule_id,))
                    
                    connect.commit()
                    
                    # Show booking confirmation
                    booking_id = cursor.lastrowid
                    messagebox.showinfo("Success", 
                                      f"Booking Confirmed!\n\n"
                                      f"Booking ID: {booking_id}\n"
                                      f"From: {source}\n"
                                      f"To: {destination}\n"
                                      f"Date: {departure_date}\n"
                                      f"Time: {departure_time}\n"
                                      f"Bus: {bus_number}\n"
                                      f"Fare: Rs. {fare}")
                    
                    # Refresh the search results
                    display_buses()
                    
                except Exception as e:
                    connect.rollback()
                    messagebox.showerror("Error", f"Failed to book ticket: {str(e)}")
                finally:
                    cursor.close()
                    connect.close()

    def cancel_booking(booking_id, schedule_id, callback=None):
        # Create cancellation reason selector window
        reason_window = ctk.CTkToplevel()
        reason_window.title("Cancel Booking")
        reason_window.geometry("400x500")
        
        # Center the window
        reason_window.update_idletasks()
        width = reason_window.winfo_width()
        height = reason_window.winfo_height()
        x = (reason_window.winfo_screenwidth() // 2) - (width // 2)
        y = (reason_window.winfo_screenheight() // 2) - (height // 2)
        reason_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make main window wait for this window
        reason_window.grab_set()
        
        # Title
        title_label = ctk.CTkLabel(
            reason_window,
            text="Please select a reason for cancellation",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Cancellation reasons
        reasons = [
            "Change in travel plans",
            "Found better alternative",
            "Emergency situation",
            "Weather concerns",
            "Other personal reasons"
        ]
        
        selected_reason = ctk.StringVar()
        
        # Create frame for reasons
        reasons_frame = ctk.CTkFrame(reason_window, fg_color="transparent")
        reasons_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        for reason in reasons:
            radio_btn = ctk.CTkRadioButton(
                reasons_frame,
                text=reason,
                variable=selected_reason,
                value=reason,
                font=ctk.CTkFont(size=14)
            )
            radio_btn.pack(pady=10, anchor="w")
        
        def process_cancellation():
            if not selected_reason.get():
                messagebox.showerror("Error", "Please select a reason for cancellation")
                return
                
            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    # Start transaction
                    connect.start_transaction()
                    
                    # Update booking status with cancellation reason
                    cursor.execute("""
                        UPDATE bookings 
                        SET status = 'Cancelled',
                            cancellation_reason = %s,
                            cancellation_date = CURDATE()
                        WHERE booking_id = %s
                    """, (selected_reason.get(), booking_id))
                    
                    # Increase available seats
                    cursor.execute("""
                        UPDATE schedules 
                        SET available_seats = available_seats + 1 
                        WHERE schedule_id = %s
                    """, (schedule_id,))
                    
                    connect.commit()
                    messagebox.showinfo("Success", "Booking cancelled successfully!")
                    
                    # Close the reason window
                    reason_window.destroy()
                    
                    # Refresh the view
                    if callback:
                        callback()
                    
                except Exception as e:
                    connect.rollback()
                    messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")
                finally:
                    cursor.close()
                    connect.close()
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(reason_window, fg_color="transparent")
        buttons_frame.pack(pady=20, padx=20, fill="x")
        
        # Cancel button (closes window)
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Back",
            width=100,
            command=reason_window.destroy
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Confirm button
        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Confirm Cancellation",
            width=150,
            fg_color="red",
            hover_color="#8B0000",
            command=process_cancellation
        )
        confirm_btn.pack(side="right", padx=10)

    def my_bookings():
        # Clear main content
        for widget in main_content.winfo_children():
            widget.destroy()
            
        # Create header
        header_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20,0))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="My Bookings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
        
        # Create scrollable frame for bookings
        bookings_frame = ctk.CTkScrollableFrame(main_content)
        bookings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        def load_bookings():
            # Clear existing bookings
            for widget in bookings_frame.winfo_children():
                widget.destroy()
                
            # Create headers with fixed widths
            headers = [
                ("Booking ID", 150),
                ("Bus", 100),
                ("From", 100),
                ("To", 100),
                ("Date", 100),
                ("Time", 100),
                ("Amount", 100),
                ("Status", 100),
                ("Actions", 150)
            ]
            
            header_frame = ctk.CTkFrame(bookings_frame)
            header_frame.pack(fill="x", pady=(0, 10))
            
            for col, (header, width) in enumerate(headers):
                label = ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    width=width
                )
                label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
            
            # Get user's bookings
            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    cursor.execute("""
                        SELECT 
                            b.booking_id,
                            bs.bus_number,
                            r.source_city,
                            r.destination_city,
                            s.departure_date,
                            s.departure_time,
                            b.total_amount,
                            b.status,
                            s.schedule_id
                        FROM bookings b
                        JOIN schedules s ON b.schedule_id = s.schedule_id
                        JOIN routes r ON s.route_id = r.route_id
                        JOIN buses bs ON s.bus_id = bs.bus_id
                        WHERE b.user_id = %s
                        ORDER BY s.departure_date DESC, s.departure_time DESC
                    """, (user_id,))
                    
                    bookings = cursor.fetchall()
                    
                    if not bookings:
                        no_data_label = ctk.CTkLabel(
                            bookings_frame,
                            text="No bookings found",
                            font=ctk.CTkFont(size=14)
                        )
                        no_data_label.pack(pady=20)
                        return
                    
                    for booking in bookings:
                        row_frame = ctk.CTkFrame(bookings_frame)
                        row_frame.pack(fill="x", pady=2)
                        
                        # Format date and time
                        date_str = booking[4].strftime('%Y-%m-%d')
                        time_obj = datetime.strptime(str(booking[5]), '%H:%M:%S')
                        time_str = time_obj.strftime('%I:%M %p')
                        
                        # Display values
                        values = [
                            f"BUS-{booking[1]}-{booking[0]}",  # Booking ID
                            booking[1],                         # Bus number
                            booking[2],                         # Source
                            booking[3],                         # Destination
                            date_str,                          # Date
                            time_str,                          # Time
                            f"Rs. {booking[6]}",               # Amount
                            booking[7]                          # Status
                        ]
                        
                        for col, (value, (_, width)) in enumerate(zip(values, headers[:-1])):
                            label = ctk.CTkLabel(
                                row_frame,
                                text=str(value),
                                font=ctk.CTkFont(size=13),
                                width=width
                            )
                            label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
                        
                        # Add action buttons
                        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                        action_frame.grid(row=0, column=len(values), padx=5, pady=5)
                        
                        # Only show cancel button for confirmed bookings and future dates
                        if booking[7] == "Confirmed" and booking[4] >= datetime.now().date():
                            cancel_btn = ctk.CTkButton(
                                action_frame,
                                text="Cancel",
                                width=80,
                                height=25,
                                fg_color="red",
                                hover_color="#8B0000",
                                command=lambda b_id=booking[0], s_id=booking[8]: 
                                    cancel_booking(b_id, s_id, load_bookings)
                            )
                            cancel_btn.pack(side="left", padx=5)
                        
                        print_btn = ctk.CTkButton(
                            action_frame,
                            text="Print",
                            width=80,
                            height=25,
                            command=lambda b=booking: print_ticket(b)
                        )
                        print_btn.pack(side="left", padx=5)
                        
                except Exception as e:
                    print(f"Error fetching bookings: {e}")
                    error_label = ctk.CTkLabel(
                        bookings_frame,
                        text=f"Error loading bookings: {str(e)}",
                        text_color="red"
                    )
                    error_label.pack(pady=20)
                finally:
                    cursor.close()
                    connect.close()
        
        # Initial load
        load_bookings()

    def manage_buses():
        if not is_admin:
            messagebox.showerror("Error", "Access Denied")
            return
            
        # Clear main content
        for widget in main_content.winfo_children():
            widget.destroy()
            
        # Add bus management interface
        header = ctk.CTkLabel(main_content, 
                            text="Manage Buses",
                            font=ctk.CTkFont(size=24, weight="bold"))
        header.pack(pady=20)
        
        # Add bus form
        form_frame = ctk.CTkFrame(main_content)
        form_frame.pack(fill="x", padx=20, pady=10)

        # Create form fields
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(padx=20, pady=20)

        # Bus Number
        ctk.CTkLabel(fields_frame, text="Bus Number:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        bus_number = ctk.CTkEntry(fields_frame, width=200)
        bus_number.grid(row=0, column=1, padx=10, pady=5)

        # Bus Name (with predefined options)
        ctk.CTkLabel(fields_frame, text="Bus Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        bus_operators = [
            "Prithivi Yatayat",
            "Saugat Yatayat",
            "Rider Yatayat"
        ]
        bus_name_var = ctk.StringVar()
        bus_name_dropdown = ctk.CTkComboBox(
            fields_frame, 
            width=200, 
            variable=bus_name_var,
            values=bus_operators
        )
        bus_name_dropdown.set(bus_operators[0])  # Set default value
        bus_name_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Bus Type
        ctk.CTkLabel(fields_frame, text="Bus Type:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        bus_type = ctk.CTkComboBox(fields_frame, values=["AC", "Non-AC"], width=200)
        bus_type.grid(row=2, column=1, padx=10, pady=5)

        # Total Seats
        ctk.CTkLabel(fields_frame, text="Total Seats:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        total_seats = ctk.CTkEntry(fields_frame, width=200)
        total_seats.grid(row=3, column=1, padx=10, pady=5)

        def add_bus():
            # Get values from form
            number = bus_number.get()
            name = bus_name_var.get()
            type_ = bus_type.get()
            seats = total_seats.get()

            # Validate inputs
            if not all([number, name, type_, seats]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                seats = int(seats)
                if seats <= 0:
                    messagebox.showerror("Error", "Total seats must be a positive number!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Total seats must be a number!")
                return

            # Add to database
            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    # Insert new bus
                    query = """
                        INSERT INTO buses (bus_number, bus_name, bus_type, total_seats, is_active) 
                        VALUES (%s, %s, %s, %s, TRUE)
                    """
                    cursor.execute(query, (number, name, type_, seats))
                    connect.commit()
                    messagebox.showinfo("Success", "Bus added successfully!")
                    
                    # Clear form fields
                    bus_number.delete(0, 'end')
                    bus_name_var.set(bus_operators[0])
                    bus_type.set("AC")
                    total_seats.delete(0, 'end')
                    
                    # Refresh bus list
                    display_buses()
                    
                except mysql.connector.IntegrityError as e:
                    if "Duplicate entry" in str(e):
                        messagebox.showerror("Error", "Bus number already exists!")
                    else:
                        messagebox.showerror("Error", f"Database error: {e}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")
                finally:
                    cursor.close()
                    connect.close()
            else:
                messagebox.showerror("Error", "Could not connect to database")

        # Add Bus Button
        add_btn = ctk.CTkButton(fields_frame, text="Add Bus", command=add_bus)
        add_btn.grid(row=4, column=0, columnspan=2, pady=20)

        # Display existing buses
        def display_buses():
            # Clear existing bus list if any
            for widget in bus_list_frame.winfo_children():
                widget.destroy()

            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    cursor.execute("""
                        SELECT bus_id, bus_number, bus_name, bus_type, total_seats, is_active 
                        FROM buses 
                        ORDER BY bus_id DESC
                    """)
                    buses = cursor.fetchall()

                    if buses:
                        # Headers
                        headers = ["Bus Number", "Bus Name", "Type", "Seats", "Status", "Actions"]
                        for col, header in enumerate(headers):
                            ctk.CTkLabel(bus_list_frame, 
                                       text=header,
                                      font=ctk.CTkFont(weight="bold")).grid(row=0, column=col, padx=10, pady=5)
                            

                        # Bus data
                        for row, bus in enumerate(buses, start=1):
                            ctk.CTkLabel(bus_list_frame, text=bus[1]).grid(row=row, column=0, padx=10, pady=5)
                            ctk.CTkLabel(bus_list_frame, text=bus[2]).grid(row=row, column=1, padx=10, pady=5)
                            ctk.CTkLabel(bus_list_frame, text=bus[3]).grid(row=row, column=2, padx=10, pady=5)
                            ctk.CTkLabel(bus_list_frame, text=bus[4]).grid(row=row, column=3, padx=10, pady=5)
                            status = "Active" if bus[5] else "Inactive"
                            ctk.CTkLabel(bus_list_frame, text=status).grid(row=row, column=4, padx=10, pady=5)
                            
                            # Actions frame for buttons
                            actions_frame = ctk.CTkFrame(bus_list_frame, fg_color="transparent")
                            actions_frame.grid(row=row, column=5, padx=10, pady=5)
                            
                            # Edit button
                            ctk.CTkButton(
                                actions_frame,
                                text="Edit",
                                width=80,
                                command=lambda b=bus[0], data=bus: edit_bus(b, data)
                            ).pack(side="left", padx=5)

                            # Toggle active status button
                            toggle_text = "Deactivate" if bus[5] else "Activate"
                            ctk.CTkButton(
                                actions_frame,
                                text=toggle_text,
                                width=80,
                                command=lambda b=bus[0], s=bus[5]: toggle_bus_status(b, s)
                            ).pack(side="left", padx=5)

                            # Delete button
                            ctk.CTkButton(
                                actions_frame,
                                text="Delete",
                                width=80,
                                fg_color="red",
                                hover_color="#8B0000",
                                command=lambda b=bus[0]: delete_bus(b)
                            ).pack(side="left", padx=5)

                    else:
                        ctk.CTkLabel(bus_list_frame, 
                                   text="No buses found",
                                   font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=10, pady=20)

                except Exception as e:
                    print(f"Error fetching buses: {e}")
                finally:
                    cursor.close()
                    connect.close()

        def edit_bus(bus_id, current_data):
            # Create edit dialog
            edit_window = ctk.CTkToplevel()
            edit_window.title("Edit Bus")
            edit_window.geometry("400x500")
            
            # Center the window
            edit_window.update_idletasks()
            width = edit_window.winfo_width()
            height = edit_window.winfo_height()
            x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
            y = (edit_window.winfo_screenheight() // 2) - (height // 2)
            edit_window.geometry(f'{width}x{height}+{x}+{y}')
            
            # Make main window wait for this window
            edit_window.grab_set()
            
            # Create form fields
            form_frame = ctk.CTkFrame(edit_window)
            form_frame.pack(padx=20, pady=20, fill="both", expand=True)
            
            # Title
            title = ctk.CTkLabel(form_frame, 
                                text="Edit Bus Details",
                                font=ctk.CTkFont(size=20, weight="bold"))
            title.pack(pady=20)
            
            # Bus Number (readonly)
            ctk.CTkLabel(form_frame, text="Bus Number:").pack(pady=(10,0))
            bus_number = ctk.CTkEntry(form_frame, width=200)
            bus_number.insert(0, current_data[1])
            bus_number.configure(state="readonly")
            bus_number.pack(pady=(0,10))
            
            # Bus Name in edit window
            ctk.CTkLabel(form_frame, text="Bus Name:").pack(pady=(10,0))
            bus_name_var = ctk.StringVar()
            bus_name_dropdown = ctk.CTkComboBox(
                form_frame, 
                width=200, 
                variable=bus_name_var,
                values=bus_operators
            )
            if current_data[2] in bus_operators:
                bus_name_dropdown.set(current_data[2])
            else:
                bus_name_dropdown.set(bus_operators[0])
            bus_name_dropdown.pack(pady=(0,10))
            
            # Bus Type
            ctk.CTkLabel(form_frame, text="Bus Type:").pack(pady=(10,0))
            bus_type = ctk.CTkComboBox(form_frame, values=["AC", "Non-AC"], width=200)
            bus_type.set(current_data[3])
            bus_type.pack(pady=(0,10))
            
            # Total Seats
            ctk.CTkLabel(form_frame, text="Total Seats:").pack(pady=(10,0))
            total_seats = ctk.CTkEntry(form_frame, width=200)
            total_seats.insert(0, str(current_data[4]))
            total_seats.pack(pady=(0,10))

            def save_changes():
                # Validate inputs
                name = bus_name_var.get()
                type_ = bus_type.get()
                seats = total_seats.get()

                if not all([name, type_, seats]):
                    messagebox.showerror("Error", "All fields are required!", parent=edit_window)
                    return

                try:
                    seats = int(seats)
                    if seats <= 0:
                        messagebox.showerror("Error", "Total seats must be a positive number!", parent=edit_window)
                        return
                except ValueError:
                    messagebox.showerror("Error", "Total seats must be a number!", parent=edit_window)
                    return

                # Update database
                connect = connect_mysql()
                if connect:
                    cursor = connect.cursor()
                    try:
                        query = """
                            UPDATE buses 
                            SET bus_name = %s, bus_type = %s, total_seats = %s 
                            WHERE bus_id = %s
                        """
                        cursor.execute(query, (name, type_, seats, bus_id))
                        connect.commit()
                        messagebox.showinfo("Success", "Bus details updated successfully!", parent=edit_window)
                        edit_window.destroy()
                        display_buses()  # Refresh the list
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to update bus details: {e}", parent=edit_window)
                    finally:
                        cursor.close()
                        connect.close()

            # Save and Cancel buttons
            buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            buttons_frame.pack(pady=20)
            
            ctk.CTkButton(buttons_frame, 
                         text="Save Changes",
                         command=save_changes).pack(side="left", padx=10)
                         
            ctk.CTkButton(buttons_frame, 
                         text="Cancel",
                         command=edit_window.destroy).pack(side="left", padx=10)

        def delete_bus(bus_id):
            # Ask for confirmation
            if not messagebox.askyesno("Confirm Delete", 
                                     "Are you sure you want to delete this bus? This action cannot be undone."):
                return

            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    # First check if the bus has any associated schedules
                    cursor.execute("SELECT COUNT(*) FROM schedules WHERE bus_id = %s", (bus_id,))
                    schedule_count = cursor.fetchone()[0]
                    
                    if schedule_count > 0:
                        messagebox.showerror(
                            "Error", 
                            "Cannot delete this bus as it has associated schedules. Deactivate it instead."
                        )
                        return

                    # If no schedules, proceed with deletion
                    cursor.execute("DELETE FROM buses WHERE bus_id = %s", (bus_id,))
                    connect.commit()
                    messagebox.showinfo("Success", "Bus deleted successfully!")
                    display_buses()  # Refresh the list
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete bus: {e}")
                finally:
                    cursor.close()
                    connect.close()

        def toggle_bus_status(bus_id, current_status):
            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    new_status = not current_status
                    cursor.execute("UPDATE buses SET is_active = %s WHERE bus_id = %s", 
                                 (new_status, bus_id))
                    connect.commit()
                    messagebox.showinfo(
                        "Success", 
                        f"Bus {'activated' if new_status else 'deactivated'} successfully!"
                    )
                    display_buses()  # Refresh the list
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update bus status: {e}")
                finally:
                    cursor.close()
                    connect.close()

        # Create frame for bus list
        list_label = ctk.CTkLabel(main_content, 
                                 text="Existing Buses",
                                 font=ctk.CTkFont(size=20, weight="bold"))
        list_label.pack(pady=(20, 10))

        bus_list_frame = ctk.CTkFrame(main_content)
        bus_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Display initial bus list
        display_buses()

    def manage_routes():
        if not is_admin:
            messagebox.showerror("Error", "Access Denied")
            return
            
        # Clear main content
        for widget in main_content.winfo_children():
            widget.destroy()
            
        # Create header frame with title and add button
        header_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20,0))
        
        # Title on left
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Manage Routes",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
        
        # Add Route button on right
        add_route_btn = ctk.CTkButton(
            header_frame,
            text="+ Add New Route",
            command=lambda: open_add_route_window(),
            width=150,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2ECC71",
            hover_color="#27AE60"
        )
        add_route_btn.pack(side="right")

        # Create frame for route list
        route_list_frame = ctk.CTkFrame(main_content)
        route_list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        def open_add_route_window():
            add_window = ctk.CTkToplevel()
            add_window.title("Add New Route")
            add_window.geometry("500x700")
            
            # Center window
            add_window.update_idletasks()
            width = add_window.winfo_width()
            height = add_window.winfo_height()
            x = (add_window.winfo_screenwidth() // 2) - (width // 2)
            y = (add_window.winfo_screenheight() // 2) - (height // 2)
            add_window.geometry(f'{width}x{height}+{x}+{y}')
            add_window.grab_set()
            
            # Create main frame
            main_frame = ctk.CTkFrame(add_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Title
            title = ctk.CTkLabel(
                main_frame, 
                text="Add New Route",
                font=ctk.CTkFont(size=20, weight="bold")
            )
            title.pack(pady=20)

            # Create form frame
            form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            form_frame.pack(fill="x", padx=20)

            # Source City
            ctk.CTkLabel(form_frame, text="Source City:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(10,0))
            source_var = ctk.StringVar()
            source_dropdown = ctk.CTkComboBox(form_frame, variable=source_var, width=400)
            source_dropdown.pack(fill="x", pady=(0,10))

            # Destination City
            ctk.CTkLabel(form_frame, text="Destination City:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(10,0))
            dest_var = ctk.StringVar()
            dest_dropdown = ctk.CTkComboBox(form_frame, variable=dest_var, width=400)
            dest_dropdown.pack(fill="x", pady=(0,10))

            # Bus Selection
            ctk.CTkLabel(form_frame, text="Select Bus:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(10,0))
            bus_var = ctk.StringVar()
            bus_dropdown = ctk.CTkComboBox(form_frame, variable=bus_var, width=400)
            bus_dropdown.pack(fill="x", pady=(0,10))

            # Fare
            ctk.CTkLabel(form_frame, text="Fare (Rs.):", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(10,0))
            fare = ctk.CTkEntry(form_frame, width=400, placeholder_text="Enter fare amount")
            fare.pack(fill="x", pady=(0,10))

            # Date (Using separate dropdowns for year, month, day)
            date_label = ctk.CTkLabel(form_frame, text="Departure Date:", font=ctk.CTkFont(size=14))
            date_label.pack(anchor="w", pady=(10,0))
            
            date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            date_frame.pack(fill="x", pady=(0,10))

            # Year dropdown
            current_year = datetime.now().year
            years = [str(year) for year in range(current_year, current_year + 2)]
            year_var = ctk.StringVar(value=str(current_year))
            year_dropdown = ctk.CTkComboBox(date_frame, values=years, variable=year_var, width=120)
            year_dropdown.pack(side="left", padx=5)

            # Month dropdown
            months = [f"{i:02d}" for i in range(1, 13)]
            month_var = ctk.StringVar(value=f"{datetime.now().month:02d}")
            month_dropdown = ctk.CTkComboBox(date_frame, values=months, variable=month_var, width=120)
            month_dropdown.pack(side="left", padx=5)

            # Day dropdown
            days = [f"{i:02d}" for i in range(1, 32)]
            day_var = ctk.StringVar(value=f"{datetime.now().day:02d}")
            day_dropdown = ctk.CTkComboBox(date_frame, values=days, variable=day_var, width=120)
            day_dropdown.pack(side="left", padx=5)

            # Time Frame
            time_label = ctk.CTkLabel(form_frame, text="Departure Time:", font=ctk.CTkFont(size=14))
            time_label.pack(anchor="w", pady=(10,0))
            
            time_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            time_frame.pack(fill="x", pady=(0,10))

            # Hour
            hour_var = ctk.StringVar(value="01")
            hour_dropdown = ctk.CTkComboBox(
                time_frame,
                width=120,
                variable=hour_var,
                values=[f"{i:02d}" for i in range(1, 13)]
            )
            hour_dropdown.pack(side="left", padx=5)

            # Minute
            minute_var = ctk.StringVar(value="00")
            minute_dropdown = ctk.CTkComboBox(
                time_frame,
                width=120,
                variable=minute_var,
                values=[f"{i:02d}" for i in range(60)]
            )
            minute_dropdown.pack(side="left", padx=5)

            # AM/PM
            ampm_var = ctk.StringVar(value="AM")
            ampm_dropdown = ctk.CTkComboBox(
                time_frame,
                width=120,
                variable=ampm_var,
                values=["AM", "PM"]
            )
            ampm_dropdown.pack(side="left", padx=5)

            def add_route():
                # Get form values
                source = source_var.get()
                destination = dest_var.get()
                bus_info = bus_var.get()
                fare_amount = fare.get().strip()
                
                # Construct date string
                dep_date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
                
                # Get time values
                hour = hour_var.get()
                minute = minute_var.get()
                ampm = ampm_var.get()

                # Validate inputs
                if not all([source, destination, bus_info, fare_amount]):
                    messagebox.showerror("Error", "All fields are required!", parent=add_window)
                    return

                if source == destination:
                    messagebox.showerror("Error", "Source and destination cannot be the same!", parent=add_window)
                    return

                try:
                    fare_amount = float(fare_amount)
                    if fare_amount <= 0:
                        messagebox.showerror("Error", "Fare must be a positive number!", parent=add_window)
                        return
                except ValueError:
                    messagebox.showerror("Error", "Fare must be a number!", parent=add_window)
                    return

                # Validate date
                try:
                    dep_date_obj = datetime.strptime(dep_date, '%Y-%m-%d')
                    if dep_date_obj.date() < datetime.now().date():
                        messagebox.showerror("Error", "Departure date cannot be in the past!", parent=add_window)
                        return
                except ValueError:
                    messagebox.showerror("Error", "Invalid date!", parent=add_window)
                    return

                # Convert time to 24-hour format
                hour = int(hour)
                minute = int(minute)
                if ampm == "PM" and hour != 12:
                    hour += 12
                elif ampm == "AM" and hour == 12:
                    hour = 0
                departure_time = f"{hour:02d}:{minute:02d}:00"

                # Extract bus number
                try:
                    bus_number = bus_info.split(" - ")[0]
                except:
                    messagebox.showerror("Error", "Invalid bus selection!", parent=add_window)
                    return

                # Add to database
                connect = connect_mysql()
                if connect:
                    cursor = connect.cursor()
                    try:
                        # Start transaction
                        connect.start_transaction()

                        # Get bus_id and seats
                        cursor.execute("SELECT bus_id, total_seats FROM buses WHERE bus_number = %s", (bus_number,))
                        bus_result = cursor.fetchone()
                        if not bus_result:
                            raise Exception("Selected bus not found!")
                        bus_id, total_seats = bus_result

                        # Insert route
                        cursor.execute("""
                            INSERT INTO routes (source_city, destination_city, fare, is_active) 
                            VALUES (%s, %s, %s, TRUE)
                        """, (source, destination, fare_amount))
                        route_id = cursor.lastrowid

                        # Insert schedule
                        cursor.execute("""
                            INSERT INTO schedules (route_id, bus_id, departure_date, departure_time, 
                                                 available_seats, is_active)
                            VALUES (%s, %s, %s, %s, %s, TRUE)
                        """, (route_id, bus_id, dep_date, departure_time, total_seats))

                        connect.commit()
                        messagebox.showinfo("Success", "Route added successfully!", parent=add_window)
                        add_window.destroy()
                        refresh_routes_display()  # Refresh route list

                    except Exception as e:
                        connect.rollback()
                        messagebox.showerror("Error", f"Failed to add route: {str(e)}", parent=add_window)
                    finally:
                        cursor.close()
                        connect.close()

            # Buttons frame at the bottom
            buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", pady=20)

            # Add Button
            add_btn = ctk.CTkButton(
                buttons_frame,
                text="Add Route",
                command=add_route,
                width=150,
                height=35,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#2ECC71",
                hover_color="#27AE60"
            )
            add_btn.pack(side="left", padx=10)

            # Cancel Button
            cancel_btn = ctk.CTkButton(
                buttons_frame,
                text="Cancel",
                command=add_window.destroy,
                width=150,
                height=35,
                font=ctk.CTkFont(size=14),
                fg_color="#E74C3C",
                hover_color="#C0392B"
            )
            cancel_btn.pack(side="right", padx=10)

            # Load cities and buses
            def load_active_cities():
                connect = connect_mysql()
                if connect:
                    cursor = connect.cursor()
                    try:
                        cursor.execute("""
                            SELECT city_name 
                            FROM cities 
                            WHERE is_active = TRUE 
                            ORDER BY city_name
                        """)
                        cities = [city[0] for city in cursor.fetchall()]
                        if cities:
                            source_dropdown.configure(values=cities)
                            source_dropdown.set(cities[0])
                            update_destination_cities()
                        else:
                            messagebox.showerror("Error", "No active cities found!", parent=add_window)
                    finally:
                        cursor.close()
                        connect.close()

            def update_destination_cities(*args):
                selected_source = source_var.get()
                connect = connect_mysql()
                if connect:
                    cursor = connect.cursor()
                    try:
                        cursor.execute("""
                            SELECT city_name 
                            FROM cities 
                            WHERE is_active = TRUE AND city_name != %s
                            ORDER BY city_name
                        """, (selected_source,))
                        cities = [city[0] for city in cursor.fetchall()]
                        dest_dropdown.configure(values=cities)
                        if cities:
                            dest_dropdown.set(cities[0])
                    finally:
                        cursor.close()
                        connect.close()

            def load_buses():
                connect = connect_mysql()
                if connect:
                    cursor = connect.cursor()
                    try:
                        cursor.execute("""
                            SELECT bus_number, bus_name 
                            FROM buses 
                            WHERE is_active = TRUE
                            ORDER BY bus_number
                        """)
                        buses = [f"{bus[0]} - {bus[1]}" for bus in cursor.fetchall()]
                        if buses:
                            bus_dropdown.configure(values=buses)
                            bus_dropdown.set(buses[0])
                        else:
                            messagebox.showerror("Error", "No active buses found!", parent=add_window)
                    finally:
                        cursor.close()
                        connect.close()

            # Bind source city selection
            source_var.trace('w', update_destination_cities)

            # Load initial data
            load_active_cities()
            load_buses()

        def display_routes():
            # Clear existing items
            for widget in route_list_frame.winfo_children():
                widget.destroy()

            # Create scrollable frame
            scrollable_frame = create_scrollable_frame(route_list_frame)

            # Add headers
            headers = ["Route ID", "Source", "Destination", "Bus", "Date", "Time", "Fare", "Status", "Actions"]
            for col, header in enumerate(headers):
                ctk.CTkLabel(
                    scrollable_frame,
                    text=header,
                    font=ctk.CTkFont(weight="bold")
                ).grid(row=0, column=col, padx=10, pady=5, sticky="w")

            # Fetch and display routes
            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    cursor.execute("""
                        SELECT r.route_id, r.source_city, r.destination_city, 
                               b.bus_number, b.bus_name, s.departure_date, 
                               s.departure_time, r.fare, r.is_active
                        FROM routes r
                        LEFT JOIN schedules s ON r.route_id = s.route_id
                        LEFT JOIN buses b ON s.bus_id = b.bus_id
                        ORDER BY s.departure_date DESC, s.departure_time DESC
                    """)
                    routes = cursor.fetchall()

                    for row, route in enumerate(routes, start=1):
                        # Route ID
                        ctk.CTkLabel(scrollable_frame, text=route[0]).grid(
                            row=row, column=0, padx=10, pady=5, sticky="w")
                        
                        
                    
                        # Source
                        ctk.CTkLabel(scrollable_frame, text=route[1]).grid(
                            row=row, column=1, padx=10, pady=5, sticky="w")
                        
                        
                        
                        # Destination
                        ctk.CTkLabel(scrollable_frame, text=route[2]).grid(
                            row=row, column=2, padx=10, pady=5, sticky="w")
                        
                        
                        
                        # Bus
                        bus_info = f"{route[3]} - {route[4]}" if route[3] and route[4] else "Not assigned"
                        ctk.CTkLabel(scrollable_frame, text=bus_info).grid(
                            row=row, column=3, padx=10, pady=5, sticky="w")
                        
                        # Date
                        date_str = route[5].strftime('%Y-%m-%d') if route[5] else "Not set"
                        ctk.CTkLabel(scrollable_frame, text=date_str).grid(
                            row=row, column=4, padx=10, pady=5, sticky="w")
                        
                        
                        
                        # Time
                        if route[6]:
                            time_obj = datetime.strptime(str(route[6]), '%H:%M:%S')
                            time_str = time_obj.strftime('%I:%M %p')
                        else:
                            time_str = "Not set"
                        ctk.CTkLabel(scrollable_frame, text=time_str).grid(
                            row=row, column=5, padx=10, pady=5, sticky="w")
                        
                        
                        
                        # Fare
                        ctk.CTkLabel(scrollable_frame, text=f"Rs. {route[7]}").grid(
                            row=row, column=6, padx=10, pady=5, sticky="w")
                        
                        # Status
                        status = "Active" if route[8] else "Inactive"
                        ctk.CTkLabel(scrollable_frame, text=status).grid(
                            row=row, column=7, padx=10, pady=5, sticky="w")
                        
                        
                        
                        # Actions frame
                        actions_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
                        actions_frame.grid(row=row, column=8, padx=10, pady=5)
                        
                        # Edit button
                        ctk.CTkButton(
                            actions_frame,
                            text="Edit",
                            width=70,
                            command=lambda r=route[0]: edit_route(r)
                        ).pack(side="left", padx=2)
                        
                        # Toggle status button
                        toggle_text = "Deactivate" if route[8] else "Activate"
                        ctk.CTkButton(
                            actions_frame,
                            text=toggle_text,
                            width=70,
                            command=lambda r=route[0], s=route[8]: toggle_route_status(r, s)
                        ).pack(side="left", padx=2)
                        
                        
                        # Delete button
                        ctk.CTkButton(
                            actions_frame,
                            text="Delete",
                            width=70,
                            fg_color="#E74C3C",
                            hover_color="#C0392B",
                            command=lambda r=route[0]: delete_route(r)
                        ).pack(side="left", padx=2)

                except Exception as e:
                    print(f"Error fetching routes: {e}")
                    error_label = ctk.CTkLabel(
                        scrollable_frame,
                        text="Error loading routes",
                        text_color="red"
                    )
                    error_label.grid(row=1, column=0, columnspan=8, pady=20)
                finally:
                    cursor.close()
                    connect.close()

        # Display initial routes
        display_routes()

    def manage_cities():
        if not is_admin:
            messagebox.showerror("Error", "Access Denied")
            return
            
        # Clear main content
        for widget in main_content.winfo_children():
            widget.destroy()
            
        # Create header frame with title and add button
        header_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20,0))
        
        # Title on left
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Manage Cities",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
        
        # Add City button on right
        add_city_btn = ctk.CTkButton(
            header_frame,
            text="+ Add New City",
            width=150,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2ECC71",
            hover_color="#27AE60"
        )
        add_city_btn.pack(side="right")

        # Create frame for city list
        global city_list_frame
        city_list_frame = ctk.CTkFrame(main_content)
        city_list_frame.pack(fill="both", expand=True, padx=20, pady=20)

        def refresh_cities_display():
            """Smoothly refresh the cities display"""
            # Clear all existing widgets in city_list_frame first
            for widget in city_list_frame.winfo_children():
                widget.destroy()
            
            # Create new scrollable frame
            scrollable_frame = create_scrollable_frame(city_list_frame)
            
            # Add headers
            headers = ["City ID", "City Name", "Status", "Actions"]
            for col, header in enumerate(headers):
                label = ctk.CTkLabel(
                    scrollable_frame,
                    text=header,
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                label.grid(row=0, column=col, padx=20, pady=10, sticky="w")
            
            # Configure grid columns
            scrollable_frame.grid_columnconfigure(1, weight=1)
            
            # Fetch and display cities
            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    cursor.execute("""
                        SELECT city_id, city_name, is_active
                        FROM cities
                        ORDER BY city_name
                    """)
                    cities = cursor.fetchall()
                    
                    if not cities:
                        no_data_label = ctk.CTkLabel(
                            scrollable_frame,
                            text="No cities found",
                            font=ctk.CTkFont(size=14)
                        )
                        no_data_label.grid(row=1, column=0, columnspan=4, pady=20)
                        return

                    for row, city in enumerate(cities, start=1):
                        # City ID
                        ctk.CTkLabel(scrollable_frame, text=city[0]).grid(
                            row=row, column=0, padx=20, pady=5, sticky="w")
                        # City Name
                        ctk.CTkLabel(scrollable_frame, text=city[1]).grid(
                            row=row, column=1, padx=20, pady=5, sticky="w")
                        # Status
                        status = "Active" if city[2] else "Inactive"
                        ctk.CTkLabel(scrollable_frame, text=status).grid(
                            row=row, column=2, padx=20, pady=5, sticky="w")
                        
                        # Actions frame
                        actions_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
                        actions_frame.grid(row=row, column=3, padx=20, pady=5)
                        
                        # Toggle status button
                        toggle_text = "Deactivate" if city[2] else "Activate"
                        ctk.CTkButton(
                            actions_frame,
                            text=toggle_text,
                            width=90,
                            height=30,
                            command=lambda c=city[0], s=city[2]: toggle_city_status(c, s)
                        ).pack(side="left", padx=5)
                        
                        ctk.CTkButton(
                            actions_frame,
                            text="Delete",
                            width=90,
                            height=30,
                            fg_color="#E74C3C",
                            hover_color="#C0392B",
                            command=lambda c=city[0]: delete_city(c)
                        ).pack(side="left", padx=5)

                except Exception as e:
                    print(f"Error fetching cities: {e}")
                    error_label = ctk.CTkLabel(
                        scrollable_frame,
                        text=f"Error loading cities: {str(e)}",
                        text_color="red"
                    )
                    error_label.grid(row=1, column=0, columnspan=4, pady=20)
                finally:
                    cursor.close()
                    connect.close()

        def toggle_city_status(city_id, current_status):
            if messagebox.askyesno("Confirm Action", 
                                      f"Are you sure you want to {'deactivate' if current_status else 'activate'} this city?"):
                connect = connect_mysql()
                if connect:
                    cursor = connect.cursor()
                    try:
                        cursor.execute("""
                            UPDATE cities 
                            SET is_active = %s 
                            WHERE city_id = %s
                        """, (not current_status, city_id))
                        connect.commit()
                        messagebox.showinfo("Success", 
                                          f"City {'deactivated' if current_status else 'activated'} successfully!")
                        refresh_cities_display()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to update city status: {str(e)}")
                    finally:
                        cursor.close()
                        connect.close()

        def delete_city(city_id):
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this city?"):
                connect = connect_mysql()
                if connect:
                    cursor = connect.cursor()
                    try:
                        # Check if city is used in routes
                        cursor.execute("""
                            SELECT COUNT(*) FROM routes 
                            WHERE source_city = (SELECT city_name FROM cities WHERE city_id = %s)
                            OR destination_city = (SELECT city_name FROM cities WHERE city_id = %s)
                        """, (city_id, city_id))
                        if cursor.fetchone()[0] > 0:
                            messagebox.showerror("Error", 
                                               "Cannot delete this city as it is used in existing routes. Deactivate it instead.")
                            return
                            
                        cursor.execute("DELETE FROM cities WHERE city_id = %s", (city_id,))
                        connect.commit()
                        messagebox.showinfo("Success", "City deleted successfully!")
                        refresh_cities_display()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete city: {str(e)}")
                    finally:
                        cursor.close()
                        connect.close()

        def open_add_city_window():
            add_window = ctk.CTkToplevel()
            add_window.title("Add New City")
            add_window.geometry("400x250")
            
            # Center window
            add_window.update_idletasks()
            width = add_window.winfo_width()
            height = add_window.winfo_height()
            x = (add_window.winfo_screenwidth() // 2) - (width // 2)
            y = (add_window.winfo_screenheight() // 2) - (height // 2)
            add_window.geometry(f'{width}x{height}+{x}+{y}')
            add_window.grab_set()
            
            form_frame = ctk.CTkFrame(add_window)
            form_frame.pack(padx=20, pady=20, fill="both", expand=True)
            
            ctk.CTkLabel(form_frame, text="City Name:").pack(pady=(10,0))
            city_name = ctk.CTkEntry(form_frame, width=300)
            city_name.pack(pady=(0,20))

            def add_city():
                name = city_name.get().strip()
                if not name:
                    messagebox.showerror("Error", "City name is required!", parent=add_window)
                    return
                    
                connect = connect_mysql()
                if connect:
                    cursor = connect.cursor()
                    try:
                        cursor.execute("INSERT INTO cities (city_name) VALUES (%s)", (name,))
                        connect.commit()
                        add_window.destroy()
                        refresh_cities_display()
                    except mysql.connector.Error as err:
                        if err.errno == 1062:
                            messagebox.showerror("Error", "This city already exists!", parent=add_window)
                        else:
                            messagebox.showerror("Error", f"Failed to add city: {str(err)}", parent=add_window)
                    finally:
                        cursor.close()
                        connect.close()

            buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            buttons_frame.pack(pady=20)

            ctk.CTkButton(
                buttons_frame,
                text="Add City",
                command=add_city,
                width=100,
                fg_color="#2ECC71",
                hover_color="#27AE60"
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                buttons_frame,
                text="Cancel",
                command=add_window.destroy,
                width=100,
                fg_color="#E74C3C",
                hover_color="#C0392B"
            ).pack(side="left", padx=10)

        # Configure add button command
        add_city_btn.configure(command=open_add_city_window)
        
        # Initial display
        refresh_cities_display()

    # Navigation buttons
    if is_admin:
        # Admin navigation - only show admin-specific options
        search_btn = create_nav_button("SEARCH BUSES", search_buses)
        search_btn.pack(pady=10)
        
        manage_buses_btn = create_nav_button("Manage Buses", manage_buses)
        manage_buses_btn.pack(pady=10)
        
        manage_routes_btn = create_nav_button("Manage Routes", manage_routes)
        manage_routes_btn.pack(pady=10)
        
        manage_cities_btn = create_nav_button("Manage Cities", manage_cities)
        manage_cities_btn.pack(pady=10)
        
        booked_tickets_btn = create_nav_button("Booked Tickets", view_booked_tickets)
        booked_tickets_btn.pack(pady=10)
    else:
        # Regular user navigation
        home_btn = create_nav_button("HOME", search_buses)
        home_btn.pack(pady=5)
        
        search_btn = create_nav_button("SEARCH BUSES", search_buses)
        search_btn.pack(pady=5)
        
        bookings_btn = create_nav_button("MY BOOKINGS", my_bookings)
        bookings_btn.pack(pady=5)
    
    # Logout button (shown for both admin and regular users)
    logout_btn = create_nav_button("LOGOUT", logout)
    logout_btn.pack(side="bottom", pady=20)
    
    # User info at bottom of sidebar
    user_frame = ctk.CTkFrame(sidebar)
    user_frame.pack(side="bottom", pady=20)
    
    user_label = ctk.CTkLabel(user_frame,
                             text=f"Welcome, {username}",
                             font=ctk.CTkFont(size=12))
    user_label.pack()
    
    # Show search buses by default for regular users, manage buses for admin
    if is_admin:
        manage_buses()
    else:
        search_buses()
    
    screen.mainloop()

def create_scrollable_frame(parent):
    # Create a container frame
    container = ctk.CTkFrame(parent)
    container.pack(fill="both", expand=True)
    
    # Fix the canvas background color issue
    canvas = tk.Canvas(
        container,
        bg=parent._apply_appearance_mode(parent.cget("fg_color")),
        highlightthickness=0
    )
    canvas.pack(side="left", fill="both", expand=True)
    
    # Create scrollbar and link to canvas
    scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    
    scrollable_frame = ctk.CTkFrame(canvas)
    canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def configure_canvas_width(event):
        canvas.itemconfig(canvas_frame, width=event.width)
    
    scrollable_frame.bind("<Configure>", configure_scroll_region)
    canvas.bind("<Configure>", configure_canvas_width)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    return scrollable_frame

def cancel_booking(booking_id, schedule_id, callback=None):
    # Create cancellation reason selector window
    reason_window = ctk.CTkToplevel()
    reason_window.title("Cancel Booking")
    reason_window.geometry("400x500")
    
    # Center the window
    reason_window.update_idletasks()
    width = reason_window.winfo_width()
    height = reason_window.winfo_height()
    x = (reason_window.winfo_screenwidth() // 2) - (width // 2)
    y = (reason_window.winfo_screenheight() // 2) - (height // 2)
    reason_window.geometry(f'{width}x{height}+{x}+{y}')
    
    # Make main window wait for this window
    reason_window.grab_set()
    
    # Title
    title_label = ctk.CTkLabel(
        reason_window,
        text="Please select a reason for cancellation",
        font=ctk.CTkFont(size=16, weight="bold")
    )
    title_label.pack(pady=20)
    
    # Cancellation reasons
    reasons = [
        "Change in travel plans",
        "Found better alternative",
        "Emergency situation",
        "Weather concerns",
        "Other personal reasons"
    ]
    
    selected_reason = ctk.StringVar()
    
    # Create frame for reasons
    reasons_frame = ctk.CTkFrame(reason_window, fg_color="transparent")
    reasons_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    for reason in reasons:
        radio_btn = ctk.CTkRadioButton(
            reasons_frame,
            text=reason,
            variable=selected_reason,
            value=reason,
            font=ctk.CTkFont(size=14)
        )
        radio_btn.pack(pady=10, anchor="w")
    
    def process_cancellation():
        if not selected_reason.get():
            messagebox.showerror("Error", "Please select a reason for cancellation")
            return
            
        connect = connect_mysql()
        if connect:
            cursor = connect.cursor()
            try:
                # Start transaction
                connect.start_transaction()
                
                # Update booking status with cancellation reason
                cursor.execute("""
                    UPDATE bookings 
                    SET status = 'Cancelled',
                        cancellation_reason = %s,
                        cancellation_date = CURDATE()
                    WHERE booking_id = %s
                """, (selected_reason.get(), booking_id))
                
                # Increase available seats
                cursor.execute("""
                    UPDATE schedules 
                    SET available_seats = available_seats + 1 
                    WHERE schedule_id = %s
                """, (schedule_id,))
                
                connect.commit()
                messagebox.showinfo("Success", "Booking cancelled successfully!")
                
                # Close the reason window
                reason_window.destroy()
                
                # Refresh the view
                if callback:
                    callback()
                
            except Exception as e:
                connect.rollback()
                messagebox.showerror("Error", f"Failed to cancel booking: {str(e)}")
            finally:
                cursor.close()
                connect.close()
    
    # Buttons frame
    buttons_frame = ctk.CTkFrame(reason_window, fg_color="transparent")
    buttons_frame.pack(pady=20, padx=20, fill="x")
    
    # Cancel button (closes window)
    cancel_btn = ctk.CTkButton(
        buttons_frame,
        text="Back",
        width=100,
        command=reason_window.destroy
    )
    cancel_btn.pack(side="left", padx=10)
    
    # Confirm button
    confirm_btn = ctk.CTkButton(
        buttons_frame,
        text="Confirm Cancellation",
        width=150,
        fg_color="red",
        hover_color="#8B0000",
        command=process_cancellation
    )
    confirm_btn.pack(side="right", padx=10)

def view_booked_tickets():
    # Clear main content
    for widget in main_content.winfo_children():
        widget.destroy()
        
    # Create header
    header_frame = ctk.CTkFrame(main_content, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=(20,0))
    
    # Title
    title_label = ctk.CTkLabel(
        header_frame, 
        text="All Booked Tickets",
        font=ctk.CTkFont(size=24, weight="bold")
    )
    title_label.pack(side="left")
    
    # Create search/filter frame
    filter_frame = ctk.CTkFrame(main_content, fg_color="transparent")
    filter_frame.pack(fill="x", padx=20, pady=10)
    
    # Date filter
    ctk.CTkLabel(filter_frame, text="Date:").pack(side="left", padx=(0,5))
    date_var = ctk.StringVar(value="All")
    date_filter = ctk.CTkComboBox(
        filter_frame,
        values=["All", "Today", "Tomorrow", "This Week", "This Month"],
        variable=date_var,
        width=120
    )
    date_filter.pack(side="left", padx=5)
    
    # Status filter
    ctk.CTkLabel(filter_frame, text="Status:").pack(side="left", padx=(20,5))
    status_var = ctk.StringVar(value="All")
    status_filter = ctk.CTkComboBox(
        filter_frame,
        values=["All", "Confirmed", "Cancelled"],
        variable=status_var,
        width=120
    )
    status_filter.pack(side="left", padx=5)
    
    # Search box
    search_entry = ctk.CTkEntry(
        filter_frame,
        placeholder_text="Search by passenger name or phone",
        width=200
    )
    search_entry.pack(side="left", padx=20)
    
    # Create scrollable frame for bookings
    bookings_frame = ctk.CTkScrollableFrame(main_content)
    bookings_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def load_bookings():
        # Clear existing bookings
        for widget in bookings_frame.winfo_children():
            widget.destroy()
            
        # Create headers with fixed widths
        headers = [
            ("Booking ID", 150),
            ("Passenger", 150),
            ("Bus", 100),
            ("From", 100),
            ("To", 100),
            ("Date", 100),
            ("Time", 100),
            ("Amount", 100),
            ("Status", 100)
        ]
        
        header_frame = ctk.CTkFrame(bookings_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        for col, (header, width) in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=14, weight="bold"),
                width=width
            )
            label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
        
        # Build query based on filters
        query = """
            SELECT 
                b.booking_id,
                b.passenger_name,
                bs.bus_number,
                r.source_city,
                r.destination_city,
                s.departure_date,
                s.departure_time,
                b.total_amount,
                b.status
            FROM bookings b
            JOIN schedules s ON b.schedule_id = s.schedule_id
            JOIN routes r ON s.route_id = r.route_id
            JOIN buses bs ON s.bus_id = bs.bus_id
            WHERE 1=1
        """
        params = []
        
        # Add date filter
        if date_var.get() == "Today":
            query += " AND DATE(s.departure_date) = CURDATE()"
        elif date_var.get() == "Tomorrow":
            query += " AND DATE(s.departure_date) = DATE_ADD(CURDATE(), INTERVAL 1 DAY)"
        elif date_var.get() == "This Week":
            query += " AND YEARWEEK(s.departure_date) = YEARWEEK(CURDATE())"
        elif date_var.get() == "This Month":
            query += " AND MONTH(s.departure_date) = MONTH(CURDATE()) AND YEAR(s.departure_date) = YEAR(CURDATE())"
        
        # Add status filter
        if status_var.get() != "All":
            query += " AND b.status = %s"
            params.append(status_var.get())
        
        # Add search filter
        search_term = search_entry.get().strip()
        if search_term:
            query += """ AND (
                b.passenger_name LIKE %s 
                OR b.passenger_phone LIKE %s
            )"""
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern])
        
        query += " ORDER BY b.booking_date DESC, b.booking_id DESC"
        
        # Execute query
        connect = connect_mysql()
        if connect:
            cursor = connect.cursor()
            try:
                cursor.execute(query, tuple(params))
                bookings = cursor.fetchall()
                
                if not bookings:
                    no_data_label = ctk.CTkLabel(
                        bookings_frame,
                        text="No bookings found",
                        font=ctk.CTkFont(size=14)
                    )
                    no_data_label.pack(pady=20)
                    return
                
                for booking in bookings:
                    row_frame = ctk.CTkFrame(bookings_frame)
                    row_frame.pack(fill="x", pady=2)
                    
                    # Format date and time
                    date_str = booking[5].strftime('%Y-%m-%d')
                    time_obj = datetime.strptime(str(booking[6]), '%H:%M:%S')
                    time_str = time_obj.strftime('%I:%M %p')
                    
                    # Display values with fixed widths
                    values = [
                        f"BUS-{booking[2]}-{booking[0]}",  # Booking ID
                        booking[1],                         # Passenger name
                        booking[2],                         # Bus number
                        booking[3],                         # Source
                        booking[4],                         # Destination
                        date_str,                          # Date
                        time_str,                          # Time
                        f"Rs. {booking[7]}",               # Amount
                        booking[8]                          # Status
                    ]
                    
                    for col, (value, (_, width)) in enumerate(zip(values, headers)):
                        label = ctk.CTkLabel(
                            row_frame,
                            text=str(value),
                            font=ctk.CTkFont(size=13),
                            width=width
                        )
                        label.grid(row=0, column=col, padx=5, pady=5, sticky="w")
                    
            except Exception as e:
                print(f"Error fetching bookings: {e}")
                error_label = ctk.CTkLabel(
                    bookings_frame,
                    text=f"Error loading bookings: {str(e)}",
                    text_color="red"
                )
                error_label.pack(pady=20)
            finally:
                cursor.close()
                connect.close()
    
    # Add search/refresh button
    search_btn = ctk.CTkButton(
        filter_frame,
        text="Search",
        command=load_bookings,
        width=100
    )
    search_btn.pack(side="left", padx=5)
    
    # Initial load
    load_bookings()

def update_database_structure():
    connect = connect_mysql()
    if connect:
        cursor = connect.cursor()
        try:
            # First check if the status column exists
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = 'bus_sewa'
                AND TABLE_NAME = 'bookings'
                AND COLUMN_NAME = 'status'
            """)
            status_exists = cursor.fetchone()[0]

            if not status_exists:
                cursor.execute("""
                    ALTER TABLE bookings 
                    ADD COLUMN status VARCHAR(20) DEFAULT 'Confirmed'
                """)

            # Update NULL statuses to 'Confirmed'
            cursor.execute("""
                UPDATE bookings 
                SET status = 'Confirmed' 
                WHERE status IS NULL
            """)
            
            # Modify total_amount column
            cursor.execute("""
                ALTER TABLE bookings 
                MODIFY COLUMN total_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00
            """)

            # Check if cancellation_reason column exists
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = 'bus_sewa'
                AND TABLE_NAME = 'bookings'
                AND COLUMN_NAME = 'cancellation_reason'
            """)
            cancellation_reason_exists = cursor.fetchone()[0]

            if not cancellation_reason_exists:
                cursor.execute("""
                    ALTER TABLE bookings 
                    ADD COLUMN cancellation_reason VARCHAR(100) DEFAULT NULL,
                    ADD COLUMN cancellation_date DATE DEFAULT NULL
                """)
            
            connect.commit()
            print("Database structure updated successfully!")
            
        except Exception as e:
            print(f"Error updating database: {e}")
            connect.rollback()
        finally:
            cursor.close()
            connect.close()

def process_booking(schedule_id, bus_number, source, destination, date, time, fare):
    # Create booking window
    booking_window = ctk.CTkToplevel()
    booking_window.title("Book Ticket")
    booking_window.geometry("500x600")
    
    # Center window
    booking_window.update_idletasks()
    width = booking_window.winfo_width()
    height = booking_window.winfo_height()
    x = (booking_window.winfo_screenwidth() // 2) - (width // 2)
    y = (booking_window.winfo_screenheight() // 2) - (height // 2)
    booking_window.geometry(f'{width}x{height}+{x}+{y}')
    booking_window.grab_set()
    
    # Create main frame
    main_frame = ctk.CTkFrame(booking_window)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    # Title
    title_label = ctk.CTkLabel(
        main_frame,
        text="Passenger Information",
        font=ctk.CTkFont(size=20, weight="bold")
    )
    title_label.pack(pady=(0,20))
    
    # Journey details
    journey_frame = ctk.CTkFrame(main_frame)
    journey_frame.pack(fill="x", padx=10, pady=(0,20))
    
    ctk.CTkLabel(journey_frame, text=f"Bus: {bus_number}").pack(anchor="w")
    ctk.CTkLabel(journey_frame, text=f"From: {source}").pack(anchor="w")
    ctk.CTkLabel(journey_frame, text=f"To: {destination}").pack(anchor="w")
    ctk.CTkLabel(journey_frame, text=f"Date: {date}").pack(anchor="w")
    ctk.CTkLabel(journey_frame, text=f"Time: {time}").pack(anchor="w")
    ctk.CTkLabel(journey_frame, text=f"Fare: Rs. {fare}").pack(anchor="w")
    
    # Get available seats
    connect = connect_mysql()
    available_seats = []
    if connect:
        cursor = connect.cursor()
        try:
            # Get total seats and available seats
            cursor.execute("""
                SELECT b.total_seats, s.available_seats
                FROM schedules s
                JOIN buses b ON s.bus_id = b.bus_id
                WHERE s.schedule_id = %s
            """, (schedule_id,))
            total_seats, available_count = cursor.fetchone()
            
            # Get booked seats
            cursor.execute("""
                SELECT seat_number 
                FROM bookings 
                WHERE schedule_id = %s AND status = 'Confirmed'
            """, (schedule_id,))
            booked_seats = [row[0] for row in cursor.fetchall()]
            
            # Calculate available seats
            available_seats = [str(i) for i in range(1, total_seats + 1) 
                             if str(i) not in booked_seats]
        finally:
            cursor.close()
            connect.close()
    
    # Passenger information form
    form_frame = ctk.CTkFrame(main_frame)
    form_frame.pack(fill="x", padx=10, pady=10)
    
    ctk.CTkLabel(form_frame, text="Full Name:").pack(anchor="w")
    name_entry = ctk.CTkEntry(form_frame, width=300)
    name_entry.pack(pady=(0,10))
    name_entry.insert(0, username)  # Pre-fill with logged-in username
    
    ctk.CTkLabel(form_frame, text="Phone Number:").pack(anchor="w")
    phone_entry = ctk.CTkEntry(form_frame, width=300)
    phone_entry.pack(pady=(0,10))
    
    ctk.CTkLabel(form_frame, text="Select Seat:").pack(anchor="w")
    seat_var = ctk.StringVar()
    seat_dropdown = ctk.CTkComboBox(
        form_frame,
        values=available_seats,
        variable=seat_var,
        width=300
    )
    seat_dropdown.pack(pady=(0,20))
    
    # Available seats info
    ctk.CTkLabel(
        form_frame,
        text=f"Available Seats: {len(available_seats)}",
        font=ctk.CTkFont(weight="bold")
    ).pack()
    
    def confirm_booking():
        # Validate inputs
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        seat = seat_var.get()
        
        if not all([name, phone, seat]):
            messagebox.showerror("Error", "Please fill all fields!", parent=booking_window)
            return
        
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Error", "Please enter a valid phone number!", parent=booking_window)
            return
        
        # Confirm with user
        confirm = messagebox.askyesno("Confirm Booking", 
                                    f"Confirm booking for:\n\n"
                                    f"Name: {name}\n"
                                    f"Phone: {phone}\n"
                                    f"Seat: {seat}\n"
                                    f"Amount: Rs. {fare}",
                                    parent=booking_window)
        
        if confirm:
            connect = connect_mysql()
            if connect:
                cursor = connect.cursor()
                try:
                    # Start transaction
                    connect.start_transaction()
                    
                    # Insert booking
                    cursor.execute("""
                        INSERT INTO bookings (
                            user_id, schedule_id, booking_date, passenger_name,
                            passenger_phone, seat_number, total_amount, status
                        ) VALUES (%s, %s, CURDATE(), %s, %s, %s, %s, 'Confirmed')
                    """, (user_id, schedule_id, name, phone, seat, fare))
                    
                    # Update available seats
                    cursor.execute("""
                        UPDATE schedules 
                        SET available_seats = available_seats - 1 
                        WHERE schedule_id = %s
                    """, (schedule_id,))
                    
                    connect.commit()
                    messagebox.showinfo("Success", "Booking confirmed successfully!", parent=booking_window)
                    booking_window.destroy()
                    
                    # Refresh the bus search results
                    display_buses(source, destination, date)
                    
                except Exception as e:
                    connect.rollback()
                    messagebox.showerror("Error", f"Failed to book ticket: {str(e)}", parent=booking_window)
                finally:
                    cursor.close()
                    connect.close()
    
    # Buttons frame
    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)
    
    ctk.CTkButton(
        buttons_frame,
        text="Confirm Booking",
        command=confirm_booking,
        width=150,
        fg_color="#2ECC71",
        hover_color="#27AE60"
    ).pack(side="left", padx=10)
    
    ctk.CTkButton(
        buttons_frame,
        text="Cancel",
        command=booking_window.destroy,
        width=150,
        fg_color="#E74C3C",
        hover_color="#C0392B"
    ).pack(side="left", padx=10)

# Call this function before creating the main window
if __name__ == "__main__":
    update_database_structure()
    root = create_login_page()
    root.mainloop()
