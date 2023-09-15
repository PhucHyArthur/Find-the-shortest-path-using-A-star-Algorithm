import pygame
import math
import button
from queue import PriorityQueue

WIDTH = 600
pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
CYAN = (173, 216, 230)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col
	
	def get_color(self) : 
		return self.color

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
	
	#Kiểm tra các node lân cận
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

#Khoảng cách Manhattan
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

#Tái tạo đường đi
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

#Thuật toán A*
def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {} # Lưu trữ các nút liền trước của mỗi nút
	g_score = {spot: float("inf") for row in grid for spot in row}  # Lưu trữ giá trị g-score của mỗi nút
	g_score[start] = 0 # G-score của điểm bắt đầu được đặt là 0
	f_score = {spot: float("inf") for row in grid for spot in row} # Lưu trữ giá trị f-score của mỗi nút
	f_score[start] = h(start.get_pos(), end.get_pos()) # F-score của điểm bắt đầu được tính toán

	open_set_hash = {start} # Lưu trữ các nút đã được thêm vào hàng đợi ưu tiên

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]  # Lấy nút có ưu tiên cao nhất từ hàng đợi ưu tiên
		open_set_hash.remove(current) # Xóa nút hiện tại khỏi tập hợp các nút đã thêm vào hàng đợi ưu tiên

		if current == end: # Nếu nút hiện tại là điểm đích
			reconstruct_path(came_from, end, draw) # Tái tạo đường đi từ điểm đích về điểm bắt đầu
			end.make_end() # Đánh dấu điểm đích
			return True # Trả về True để cho biết đã tìm thấy đường đi

		for neighbor in current.neighbors: # Duyệt qua các nút láng giềng của nút hiện tại
			temp_g_score = g_score[current] + 1 # Tính toán g-score tạm thời

			if temp_g_score < g_score[neighbor]: # Nếu g-score tạm thời nhỏ hơn g-score của nút láng giềng
				came_from[neighbor] = current # Cập nhật nút liền trước của nút láng giềng
				g_score[neighbor] = temp_g_score # Cập nhật g-score của nút láng giềng
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) # Cập nhật f-score của nút láng giềng
				if neighbor not in open_set_hash: # Nếu nút láng giềng chưa có trong hàng đợi ưu tiên
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))  # Thêm nút láng giềng vào hàng đợi ưu tiên
					open_set_hash.add(neighbor) # Thêm nút láng giềng vào tập hợp các nút đã thêm vào hàng đợi ưu tiên
					neighbor.make_open() # Đánh dấu nút láng giềng là nút mở


		draw()

		if current != start:
			current.make_closed() # Đánh dấu nút hiện tại là nút đã xét

	return False # Trả về False nếu không tìm thấy đường đi

# Tạo một lưới (grid) gồm các ô (spots) có kích thước và số lượng xác định.
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows) # Tạo một ô mới với các thông số: hàng, cột, khoảng cách, số hàng
			grid[i].append(spot)
	return grid

# Vẽ lưới trên cửa sổ win với số hàng, chiều rộng và khoảng cách giữa các ô được xác định.
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # Vẽ đường ngang
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # Vẽ đường dọc

# Vẽ lưới grid
def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()
	pygame.time.delay(250)

#Xác định vị trí khi click chuột
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

#Hàm tạo level
def get_level(level, grid) : 
	my_file = open(f"level{level}.txt", "r")
	data = my_file.read() 
	new_data = []
	arr = data.split("\n")
	for row in arr : 
		row = row.replace(",", " ") 
		new_row = row.split() 
		new_data.append(new_row) 
		# print(new_row)
	for i in range(len(new_data)) : 
		for j in range(len(new_data)) : 
			if int(new_data[i][j]) == 1 : 
				grid[i][j].make_barrier()
			# if int(new_data[i][j]) == 2 : 
			# 	grid[i][j].make_start()
			# if int(new_data[i][j]) == 3 : 
			# 	grid[i][j].make_end()
	my_file.close() 

# define fonts
font = pygame.font.SysFont("arialblack",30) 
TEXT_COLOR = BLACK

def draw_text(text, font, text_color, x, y) : 
	img = font.render(text, True, text_color) 
	WIN.blit(img, (x, y))

# load button images
back_img = pygame.image.load("./images/back_button.png").convert_alpha() 
exit_img = pygame.image.load("./images/exit_button.png").convert_alpha()
level1_img = pygame.image.load("./images/level1.png").convert_alpha()
level2_img = pygame.image.load("./images/level2.png").convert_alpha() 
level3_img = pygame.image.load("./images/level3.png").convert_alpha() 

# create button instances
back_btn = button.Button(80, 400, back_img, 0.75) 
exit_btn = button.Button(330, 400, exit_img, 0.75) 
level1_btn = button.Button(80, 100, level1_img, 0.75)
level2_btn = button.Button(330, 100, level2_img, 0.19)
level3_btn = button.Button(80, 250, level3_img, 0.19)

def main(win, width):
	ROWS = 20
	grid = make_grid(ROWS, width)
	start = None
	end = None
	level = 1
	game_paused = False
	run = True
	while run:
		#win.fill(WHITE)
		if game_paused == True : 
			win.fill(CYAN)
			draw_text("Paused menu", font, TEXT_COLOR, 200, 35)
			if back_btn.draw(win) : 
				game_paused = False  

			if exit_btn.draw(win) : 
				run = False

			if level1_btn.draw(win) : 
				grid = make_grid(ROWS,width)
				level = 1
				start = None
				end = None
				game_paused = False

			if level2_btn.draw(win) : 
				grid = make_grid(ROWS, width) 
				level = 2
				start = None
				end = None
				game_paused = False

			if level3_btn.draw(win) : 
				grid = make_grid(ROWS, width) 
				level = 3
				start = None
				end = None
				game_paused = False

		else : 
			if level != 0 : 
				get_level(level,grid)
			draw(win, grid, ROWS, width)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

				if pygame.mouse.get_pressed()[0]: # LEFT
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[row][col]
					if not start and spot != end and not spot.is_barrier() :
						start = spot
						start.make_start()

					elif not end and spot != start and not spot.is_barrier() :
						end = spot
						end.make_end()

					elif spot != end and spot != start:
						spot.make_barrier()

				elif pygame.mouse.get_pressed()[2]: # RIGHT
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[row][col]
					spot.reset()
					if spot == start:
						start = None
					elif spot == end:
						end = None

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE and start and end:
						for row in grid:
							for spot in row:
								spot.update_neighbors(grid)

						algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

					if event.key == pygame.K_c:
						start = None
						end = None
						grid = make_grid(ROWS, width)
						level = 0
					
					# game pause
					if event.key == pygame.K_ESCAPE : 
						game_paused = True

					# TODO : print grid after drawing black spots to get the level (dev purpose)
					# if event.key == pygame.K_m : 
					# 	copy_grid = [[0 for x in range(len(grid))] for _ in range(len(grid))]
					# 	for i in range(len(grid)) : 
					# 		for j in range(len(grid)) : 
					# 			if grid[i][j].get_color() == BLACK : 
					# 				copy_grid[i][j] = 1 
						
					# 	for row in copy_grid : 
					# 		for spot in row : 
					# 			print(spot,end=", ")
					# 		print("")
					# 	print("end")
		
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 
				run = False
		pygame.display.update()

	pygame.quit()


main(WIN, WIDTH)