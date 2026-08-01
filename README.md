<h1 align="center">🛒 Smart Checkout — Self-Service Checkout System</h1> <p align="center">Diploma project: a desktop simulation of a self-service checkout</p> <p align="center"> <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Tkinter-GUI-3776AB?style=flat"/> <img src="https://img.shields.io/badge/Data-JSON-black?style=flat"/> <img src="https://img.shields.io/badge/status-completed-brightgreen"/> </p>

**📖 About the project**       

A Python desktop application simulating a self-service checkout in a store. It supports two modes: customer (browsing products, cart, payment, receipt) and staff (inventory management through a password-protected panel).        

Built as part of a diploma internship project.            

**Authors:** Margarita Zhogol, Egor Semkin         

**✨ Features**        
🛒 **Product catalog** with live search and product cards (name, price, stock level)          
🧺 **Shopping cart** with automatic total recalculation          
💳 **Checkout flow:** choose a payment method, generate and save a receipt to a file           
🔐 **Staff authorization** by password             
📦 **Inventory management:** add/remove products, stock level shown with a color indicator (🟢 plenty / 🟡 low / 🔴 almost out)          
💾 **Data persistence** in a JSON file — inventory data is preserved between runs           
🛡️ **Error handling:** protection against invalid input, recovery of default data if the file gets corrupted           

**🖼️ Screenshots**         

**Main menu**         
<img width="514" height="626" alt="Снимок экрана — 2026-07-31 в 17 53 59" src="https://github.com/user-attachments/assets/874b2039-6220-4439-a89d-1d5499b3296b" />      

**Product catalog and cart**        
<img width="895" height="649" alt="Снимок экрана — 2026-07-31 в 17 54 44" src="https://github.com/user-attachments/assets/38d25813-d2db-400e-8667-7bb4a0f09524" />

**Receipt**       
<img width="496" height="504" alt="Снимок экрана — 2026-07-31 в 17 55 16" src="https://github.com/user-attachments/assets/214d3e7f-5bc4-4fe8-8a1a-7d45edbbfcda" />        

**Staff panel — inventory management**         
<img width="892" height="640" alt="Снимок экрана — 2026-07-31 в 17 55 54" src="https://github.com/user-attachments/assets/fa77e1d4-5a1c-413c-9f22-572dbe30fcf0" />         
  
**🛠️ Tech stack**         
**Component** 	| **Technology**                     
Language	      | Python 3               
Interface	      | Tkinter, ttk (Treeview, Canvas + Scrollbar)              
Data storage	  | JSON               
Other	          | datetime (receipts), os (filesystem)             
 
**📁 Project structure**          
margaritazhogolkassa/                
├── kassa2.py           # main application code        
├── inventory.json      # inventory data (created automatically)             
├── receipts/           # saved receipts (created automatically)              
├── screenshots/        # screenshots for the README                    
└── README.md

**▶️ Getting started**                  
bash            
git clone https://github.com/margaritazhogol/margaritazhogolkassa.git           
cd margaritazhogolkassa           
python kassa2.py           

**Requirements:** Python 3.8+ (only standard library modules are used, no extra dependencies to install).          

**Default staff password:** 123456            

**🧪 Testing**              

The following was verified during development:          

correct and incorrect input handling (price, quantity, search)            
protection against selling more stock than is available              
data save/recovery if inventory.json is corrupted or missing           
staff authorization flow               

<p align="center">Python • Tkinter • 2026</p>               
 
