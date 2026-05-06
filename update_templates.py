import os

html_path = 'd:/Laundary/laundry_project/core/templates/core/admin_dashboard.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_layout = """<div class="row g-4 mb-5">
    <div class="col-md-4">
        <div class="glass-card text-center d-flex flex-column align-items-center justify-content-center">
            <div class="rounded-circle bg-light d-flex align-items-center justify-content-center mb-3"
                style="width: 60px; height: 60px;">
                <i class="fa-solid fa-box-open fs-3 text-primary"></i>
            </div>
            <h3 class="fw-bolder mb-0">{{ orders.count }}</h3>
            <span class="text-muted text-uppercase" style="font-size: 0.8rem; letter-spacing: 1px;">Total Orders</span>
        </div>
    </div>
    <div class="col-md-8">
        <div class="glass-card h-100">
            <h5 class="fw-bold mb-4">All Recent Orders</h5>"""

new_layout = """<div class="row g-4 mb-5">
    <div class="col-md-3">
        <div class="glass-card text-center d-flex flex-column align-items-center justify-content-center h-100 py-4">
            <div class="rounded-circle bg-light d-flex align-items-center justify-content-center mb-3"
                style="width: 60px; height: 60px;">
                <i class="fa-solid fa-box-open fs-3 text-primary"></i>
            </div>
            <h3 class="fw-bolder mb-0">{{ orders.count }}</h3>
            <span class="text-muted text-uppercase" style="font-size: 0.8rem; letter-spacing: 1px;">Total Orders</span>
        </div>
    </div>
    <div class="col-md-3">
        <div class="glass-card text-center d-flex flex-column align-items-center justify-content-center h-100 py-4">
            <div class="rounded-circle bg-light d-flex align-items-center justify-content-center mb-3"
                style="width: 60px; height: 60px;">
                <i class="fa-solid fa-indian-rupee-sign fs-3 text-success"></i>
            </div>
            <h3 class="fw-bolder mb-0 text-success">&#8377;{{ total_revenue|default:"0.00" }}</h3>
            <span class="text-muted text-uppercase" style="font-size: 0.8rem; letter-spacing: 1px;">Total Revenue</span>
        </div>
    </div>
    <div class="col-md-6">
        <div class="glass-card h-100">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h5 class="fw-bold mb-0">All Recent Orders</h5>
                <form method="GET" class="d-flex">
                    <div class="input-group">
                        <input type="text" name="search" class="form-control form-control-sm border" placeholder="Search mobile..." value="{{ search_query }}">
                        <button type="submit" class="btn btn-sm btn-primary px-3"><i class="fa-solid fa-search"></i></button>
                    </div>
                </form>
            </div>"""

old_layout = old_layout.replace('\n', '\r\n')
new_layout = new_layout.replace('\n', '\r\n')

content = content.replace(old_layout, new_layout)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done updating layout!')

# Now replace $ with ₹
files_to_update = [
    'd:/Laundary/laundry_project/core/templates/core/admin_dashboard.html',
    'd:/Laundary/laundry_project/core/templates/core/staff_dashboard.html',
    'd:/Laundary/laundry_project/core/templates/core/customer_dashboard.html',
    'd:/Laundary/laundry_project/core/templates/core/order_create.html'
]

for file_path in files_to_update:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        file_content = file_content.replace('$', '&#8377;')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        print(f'Replaced $ with ₹ in {os.path.basename(file_path)}')
