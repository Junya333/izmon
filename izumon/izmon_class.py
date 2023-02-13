'''
名前は、某ポケットなんたらにいそうでいないものを自然言語生成AIであるOpenAIを使って生成+一部手動で決めました。
self.propsにはすべてのモンスターのデータが、self.props_figには種族間によるダメージの比率が格納されています。
x方向に敵の種族が、y方向に自分の種族が対応しています。
データコードを暗号化して表示している。
'''
class Izumon:
	import random
	import time
	import hashlib
	
	player = "" #プレイヤーネーム
	iz_num = 80 #イズモンの数
	expect_damage = 80 #ダメージの期待値
	
	PROPS = [[1 , "サーファー", 0, 162, 80, 115, 153, 111, 0.4, 0], [2 , "キョーリュー", 0, 166, 154, 115, 120, 120, 0.2, 0],
			 [3 , "ササントラ", 1, 167, 125, 110, 145, 110, 0.2, 0], [4 , "トラパルト", 2, 163, 140, 95, 120, 95, 0.2, 0],
					 [5 , "マルルリ", 4, 175, 70, 100, 80, 100, 1, 0], [6 , "アーマー", 1, 173, 107, 125, 73, 105, 0.6, 0],
					 [7 , "カブリアス", 0, 183, 150, 115, 100, 105, 0.1, 0], [8 , "マスダ", 4, 151, 130, 90, 101, 90, 0.4, 0],
					 [9 , "ラウドホーン", 1, 179, 95, 120, 130, 95, 0.4, 0], [10 , "タイガイデヌ", 4, 145, 90, 80, 125, 80, 0.6, 0],
					 [11 , "バッシュドラ", 0, 183, 132, 138, 88, 92, 0.4, 0], [12 , "プロキシー", 1, 170, 85, 130, 80, 150, 0.4, 0],
					 [13 , "スプラッシュドラゴン", 3, 151, 167, 110, 80, 90, 0.4, 0], [14 , "ブラストロッキー", 2, 190, 165, 112, 95, 106, 0.2, 0],
					 [15 , "マーダードラゴン", 1, 165, 120, 90, 130, 170, 0.2, 0], [16 , "スカイスパロー", 0, 178, 113, 87, 91, 81, 0.6, 0],
					 [17 , "ファイアウォール", 4, 153, 101, 170, 94, 89, 0.4, 0], [18 , "バブルボーラー", 0, 135, 70, 90, 100, 100, 0.6, 0],
					 [19 , "バニージャンプ", 0, 145, 100, 110, 90, 100, 0.6, 0], [20 , "スノースクーパー", 1, 136, 95, 120, 105, 120, 0.6, 0],
					 [21 , "ラビットフライ", 0, 155, 115, 80, 90, 85, 0.6, 0], [22 , "スピードスター", 1, 135, 100, 95, 84, 70, 0.6, 0],
					 [23 , "フライングホッパー", 1, 115, 110, 90, 100, 80, 0.8, 0], [24 , "スターフレイム", 1, 177, 71, 122, 141, 150, 0.4, 0],
					 [25 , "プラネットポッター", 3, 138, 89, 109, 103, 115, 0.6, 0], [26 , "バイオレーサー", 2, 185, 79, 128, 149, 78, 0.4, 0],
					 [27 , "スプラッシュファイター", 1, 186, 93, 83, 98, 116, 0.6, 0], [28 , "パルネアス", 4, 165, 140, 122, 112, 129, 0.1, 0],
					 [29 , "ギガヴォルテック", 3, 178, 115, 132, 81, 124, 0.2, 0], [30 , "エンペラースライム", 4, 143, 78, 89, 106, 101, 0.8, 0],
					 [31 , "マジックチャージ", 2, 155, 107, 123, 134, 117, 0.4, 0], [32 , "バイオレイダー", 1, 178, 84, 133, 79, 92, 0.8, 0],
					 [33 , "テクノドラゴン", 1, 132, 110, 100, 122, 105, 0.6, 0], [34 , "メガヒーロー", 0, 165, 71, 83, 121, 131, 0.8, 0],
					 [35 , "プラズマテレポーター", 1, 147, 72, 85, 75, 90, 1, 0], [36 , "ナイトライダー", 1, 145, 114, 121, 106, 120, 0.4, 0],
					 [37 , "ヒートウェーブ", 1, 178, 81, 85, 73, 89, 1, 0], [38 , "プラネットストライカー", 2, 151, 87, 107, 96, 118, 0.6, 0],
					 [39 , "バードサイクロン", 1, 164, 124, 134, 80, 129, 0.2, 0], [40 , "フェイスクッカー", 0, 192, 80, 72, 84, 99, 0.8, 0],
					 [41 , "ファイヤーバード", 0, 161, 135, 118, 110, 124, 0.2, 0], [42 , "バブルフューリー", 3, 158, 94, 111, 128, 72, 0.6, 0],
					 [43 , "スカイブラスト", 0, 169, 70, 82, 134, 79, 0.8, 0], [44 , "マジックソード", 0, 159, 96, 113, 125, 121, 0.4, 0],
					 [45 , "ベイブボーラー", 2, 175, 139, 140, 131, 94, 0.1, 0], [46 , "ロックスター", 1, 144, 93, 105, 85, 101, 0.8, 0],
					 [47 , "バーチャルパワー", 0, 184, 107, 123, 137, 127, 0.2, 0], [48 , "ファイヤーフィスト", 1, 178, 137, 76, 90, 84, 0.6, 0],
					 [49 , "メタルジャイアント", 0, 138, 108, 122, 113, 92, 0.6, 0], [50 , "ナイトライトドラゴン", 1, 181, 112, 128, 72, 88, 0.6, 0],
					 [51 , "プラズマストーム", 1, 150, 116, 77, 99, 114, 0.6, 0], [52 , "ビッグバンガード", 1, 177, 118, 129, 124, 71, 0.4, 0],
					 [53 , "バーニングナイト", 1, 188, 90, 86, 136, 81, 0.6, 0], [54 , "バブルウォーカー", 0, 169, 96, 108, 128, 123, 0.4, 0],
					 [55 , "ブレイズフューリー", 3, 174, 81, 129, 73, 134, 0.6, 0], [56 , "ストームウォーカー", 1, 143, 87, 102, 119, 113, 0.8, 0],
					 [57 , "スーパーバルカン", 1, 139, 95, 120, 137, 129, 0.4, 0], [58 , "バーチャルウォリアー", 4, 177, 86, 135, 131, 76, 0.6, 0],
					 [59 , "ロックスティンガー", 1, 155, 113, 125, 72, 121, 0.4, 0], [60 , "プラネットソルジャー", 1, 182, 90, 80, 134, 84, 0.8, 0],
					 [61 , "ストームシューター", 3, 164, 100, 135, 80, 96, 0.6, 0], [62 , "ファイヤービート", 1, 152, 124, 70, 125, 140, 0.4, 0],
					 [63 , "ファイナルインパクト", 0, 130, 74, 140, 86, 101, 0.8, 0], [64 , "ヘヴィウェーブ", 0, 162, 96, 116, 134, 124, 0.4, 0],
					 [65 , "ブレイクアウトバースト", 0, 171, 134, 79, 130, 74, 0.6, 0], [66 , "ヨネ", 5, 199, 90, 100, 150, 90, 0.2, 1],
					 [67 , "ヒトシ", 5, 205, 100, 100, 140, 94, 0.2, 2], [68 , "はなえさん", 5, 162, 115, 122, 126, 151, 0.2, 3],
					 [69 , "みっちー", 5, 187, 120, 100, 100, 120, 0.2, 4], [70 , "まさよん", 5, 205, 120, 100, 90, 100, 0.2, 5],
					 [71 , "ヤングさん", 5, 195, 120, 105, 90, 100, 0.2, 6], [72 , "F澤", 5, 175, 110, 105, 110, 120, 0.2, 7],
					 [73 , "Michael", 5, 184, 126, 80, 150, 95, 0.2, 8], [74 , "加護ちゃん", 5, 155, 180, 70, 121, 99, 0.2, 9],
					 [75 , "かねちー", 5, 175, 110, 123, 107, 109, 0.2, 10], [76 , "はまりん", 5, 175, 90, 80, 120, 110, 0.2, 11],
					 [77 , "上野東京ライン", 5, 170, 100, 115, 150, 70, 0.2, 12], [78 , "ヌマカツ", 5, 185, 125, 115, 120, 100, 0.2, 13],
					 [79 , "情報の主：ヒサシ", 5, 225, 140, 140, 110, 150, 0.2, 14], [80, "泉を治めしもの", 5, 150, 100, 120, 80, 100, 0.1, 15]] #初期値
	
	race = ["文系", "理系", "SG文系", "SG理系", "理数科", "先生"] #種族名
	
	fellows = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
			   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
			   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
			   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
			   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
			   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
			   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
			   0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #仲間のデータ
	
	props_fig = [[1, 1, 0.5, 1, 0.5, 0.5],
				[1, 0.5, 0.5, 1, 1, 0.5],
				[2, 1, 0.5, 1, 1, 0.5],
				[2, 1, 1, 0.5, 1, 0.5],
				[2, 1, 1, 1, 0.5, 1],
				[2, 2, 2, 2, 0.5, 0.5]]
	
	tech_nomal = [["暗記力", "数Ⅲ","NY研修マウント", "NY研修マウント", "1年から数Ⅲ"],
	[80, 70, 85, 75, 75]] #通常攻撃
	
	TECH_SPETI = [["一橋数学", "極限","憧れのブロードウェイ", "SG探究", "叫んでもいいですか?"],
	[90, 80, 70, 70, 90]] #特殊攻撃
	
	TECH_INDIV = [["意味考えて", "世界史の窓", "声の高低差", "見えない文字", "ねぇ、%s", "ヤングドーナツ", "攻撃するしかないんですよね？", "How many points?", "常夏フィーバー", "きのこしか勝たん", "エクロジャイト", "月見バーガー", "経済学", "音声増幅プログラム", "権限Lv.100"],
				  ["証明終了", "オピニオンシート", "すーぐスマホ触る", "なぁ、%s", "センス'は'ありますよ", "地理難化", "凍り付く空気・ゑ？", "It's thinking time!", "真冬の半袖", "スペイン語の嵐", "ｺｹﾞﾝｰ", "ﾄﾞｽｶｯ、ﾄﾞｽｶｯ", "理転", "ね*100", "大雪登校"],
				  [80, 70, 90, 90, 90, 75, 90, 90, 80, 90, 80, 85, 90, 85, 120], 
				  [100, 100, 80, 80, 75, 90, 90, 100, 120, 90, 100, 130, 80, 100, 110]]
	
	MSG_SELECT = ["イズットモンスターの 世界へ ようこそ！ わしの 名前は オーキ二 みんなからは イズモン はかせと 慕われて おるよ ",
	"イズットモンスター………イズモン この 世界には イズットモンスターと 呼ばれる いきもの達が いたる所に 住んでいる! ",
	"人は イズモンたちと なかよく 遊んだり 一緒に たたかったり………… たすけあい ながら くらして いるのじゃ ",
	"しかし わしらは イズモンのすべてを 知っている わけではない イズモンの 秘密は まだまだ いっぱい ある！ ",
	"わしは それを 解き明かすために 毎日 イズモンの 研究を 続けている という わけじゃ！ ",
	"さて…… そろそろ きみの 名前を おしえて もらおう！",
	" よ イズモンを1匹も持っていないだと? しかたがない この3匹から1匹選ぶのじゃ",
	"3匹のイズモンから好きなものを選ぶのじゃ",
	"じゃな。 わかったぞ",
	" ! 準備は いいかな？ いよいよ これから きみの 物語が 始まる！ ",
	"楽しいことも 苦しいことも いっぱい きみを 待っているだろう！ 夢と 冒険と！ ",
	"イズット モンスターの 世界へ！ レッツ ゴー"]
	
	msg_split = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" #区切り
	
	def pri(self, msg : str, time : int = 4): #メッセージ表示(メッセージ, 待機秒数) 3秒がデフォルト
		print(msg)
		self.time.sleep(time)
		return
		
	def typing(self, msg : str, ty : int, num : int = 2): #各種キーボード入力
		while True:
			if ty == 1:
				data = input(msg + " -->> ")
				if data.isdigit() and 0 <= int(data) and int(data) <= num - 1:
					data = int(data)
					break
				elif data.isdigit() == False:
					print("無効な入力じゃ")
			else:
				data = str(input(msg + ">> "))
				break
		return data
		
	def set_up(self): #開始する
		print("イズットモンスター(Ver 1.00)")
		ty = self.typing("0:はじめから 1:続きから", 1)
		self.pri(self.msg_split)
		if ty == 0:
			self.select()
		else:
			while True:
				self.player = self.typing("君の名前を教えるのじゃ（セーブデータコードを持っているならその時の名前を教えるのじゃ）：", 0)
				play_type = self.typing(self.player + " よ、セーブデータコードは持っておるか？ 1:ある 0:ない", 1, 2)
				if play_type == 1:
					code = self.typing("セーブデータコード：",0)
					res = self.decode(code)
					if res == 0:
						print("無効なコードじゃ。そんな名前じゃったか?")
					else:
						break
				else:
					self.pri("コードがないのなら初めから始めるぞ")
					self.select()
					break
					
	def select(self): #開始時のイズモンを選択
		for i in range(6):
			self.pri(self.MSG_SELECT[i])
		self.player = self.typing("名前", 0)
		self.pri(self.player + self.MSG_SELECT[6])
		self.pri(self.MSG_SELECT[7])
		poc = self.typing("0:バニージャンプ 1:テクノドラゴン 2:ナイトライダー", 1, 3)
		if poc == 0:
			code = 19 - 1
		elif poc == 1:
			code = 33 - 1
		else:
			code = 36 - 1
		self.fellows[code] = 1
		self.pri(self.PROPS[code][1] + self.MSG_SELECT[8])
		self.pri("では " +self.player + self.MSG_SELECT[9])
		self.pri(self.MSG_SELECT[10])
		self.pri(self.MSG_SELECT[11])
		self.pri(self.msg_split, 5)
		return
	
	def encode(self):
		data = "1"
		hash_player = int(self.hashlib.sha256(self.player.encode("utf-8")).hexdigest(), 16)
		for i in range(100):
			if i >= self.iz_num:
				data += "0"
				continue
			data += str(self.fellos[i])
		data = str(int(data, 2))
		data += str(hash_player)[20]
		check_digit = int(data) % 9
		data += str(check_digit)
		data = format(int(data), "0x")
		return data
	
	def decode(self, code):
		hash_player = int(self.hashlib.sha256(self.player.encode("utf-8")).hexdigest(), 16)
		data = str(int(code, 16))
		if int(data) % 9 != 0:
			return 0
		data = data[:-1]
		hash_code = str(hash_player)[-20:]
		if data[-20:] != hash_code:
			return 0
		for i in range(100):
			if i >= self.iz_num:
				continue
			self.fellows[i] = data[i + 1]
		return 1
		
	def save(self): #データをセーブする
		while True:
			ty = self.typing("データをセーブしますか？ 1:する 0:しない", 1, 2)
			if ty == 1:
				code = self.encode()
				print("プレイヤー名と共に保管してください。")
				print("コード：", code)
				break
			elif ty == 0:
				print()
				break
			else:
				print()
		return
		
	def fight(self, ene : int): #バトル
		data , damage_all, tech = [], [], []
		turn = self.random.randint(0,1) #ターンを格納　0:自分 1:敵
		ene_data = self.PROPS[ene]
		print("野生の", ene_data[1], "が現れた!（HP:", ene_data[3],",種族:",self.race[ene_data[2]], "）")
		while True: #出すイズモンを選択
			me = self.typing("どれを出す？ コードで入力 (0でイズモン辞典を見る)", 1, self.iz_num) - 1
			if me == -1:
				self.dic()
			elif self.fellows[me] != 1:
				print("手持ちにいないぞ")
				continue
			else:
				break
		data, damage_all, tech = self.set(me, ene)
		while True:
			print(data[turn][1], "のターン（HP:",data[turn][2], "）")
			if turn == 0:
				while True:
					ty = self.typing("行動を選択 0:攻撃 1:特攻（残り" +str(data[0][3])+ "回）", 1, 2)
					if data[0][3] == 0 and ty == 1:
						print("残り回数がないぞ")
						continue
					elif ty == 1:
						data[0][3] -= 1
						break
					else:
						break
			else: #敵の行動を選択
				if data[1][3] == 0:
					ty = 1
				else:
					ty = self.random.randint(0, 1)
					data[1][3] -= 1
					
			self.pri(data[turn][1] + " の 攻撃", 1)
			self.pri(data[turn][1] + " の " + tech[turn][ty] + " !")
			self.pri(self.msg_split, 0)
			#命中判定
			if tech[turn + 2][ty] >= self.random.random():
				self.pri(data[abs(turn - 1)][1], "は", int(damage_all[turn][ty]), "のダメージを受けた!", 0)
				data[abs(turn - 1)][2] -= int(damage_all[turn][ty]) #ダメージ分減らす
				if data[abs(turn - 1)][2] <= 0:
					data[abs(turn - 1)][2] = 0
			else:
				self.pri("避けられた!")
			self.pri(data[abs(turn - 1)][1] + " の 残り HP :" + str(data[abs(turn - 1)][2]))
			
			self.pri(self.msg_split, 0)
			if data[0][2] <= 0:
				self.pri("HPが0になってしまった。", 2)
				break
			if data[1][2] <= 0:
				self.pri(data[1][1] + " を倒した!", 2)
				self.get(ene)
				break
			action = self.typing("どうする? 0:続ける 1:逃げる", 1, 2)
			if action == 1 and self.random.random() >= 0.8:
				self.pri("逃げられなかった")
				turn = self.turn_change(turn)
				continue
			elif action == 1:
				self.pri("逃げられた!")
				break
			turn = self.turn_change(turn)
		return
		
	def set(self, me : int, ene : int): #各種値を設定
		tech = [["", ""], ["", ""], [0, 0], [0, 0]] #技名のデータ
		damage_all = [[],[]]
		
		expect = self.expect_damage
		
		me_kind = self.PROPS[me][2] #自分の種族
		ene_kind = self.PROPS[ene][2] #敵の種族
		
		me_com = [self.PROPS[me][0], self.PROPS[me][1], self.PROPS[me][3], 10] #必要なデータのみ格納
		ene_com = [self.PROPS[ene][0], self.PROPS[ene][1],self.PROPS[ene][3], 10]
		data = [me_com, ene_com]
		
		if self.PROPS[me][9] == 0:
			tech[0][0] = self.tech_nomal[0][me_kind] #技名を格納
			tech[0][1] = self.TECH_SPETI[0][me_kind]
			tech[2][0] = self.tech_nomal[1][me_kind]
			tech[2][1] = self.TECH_SPETI[1][me_kind]
		else:
			num_tech = self.PROPS[me][9] - 1 #技番号
			tech[0][0] = self.TECH_INDIV[0][num_tech]
			tech[0][1] = self.TECH_INDIV[1][num_tech]
			tech[2][0] = self.TECH_INDIV[2][num_tech]
			tech[2][1] = self.TECH_INDIV[3][num_tech]
			
		if self.PROPS[ene][9] == 0:
			tech[1][0] = self.tech_nomal[0][me_kind] #技名を格納
			tech[1][1] = self.TECH_SPETI[0][me_kind]
			tech[3][0] = self.tech_nomal[1][me_kind]
			tech[3][1] = self.TECH_SPETI[1][me_kind]
		else:
			num_tech = self.PROPS[ene][9] - 1 #技番号
			tech[1][0] = self.TECH_INDIV[0][num_tech]
			tech[1][1] = self.TECH_INDIV[1][num_tech]
			tech[3][0] = self.TECH_INDIV[2][num_tech]
			tech[3][1] = self.TECH_INDIV[3][num_tech]
			
		if "%s" in tech[0][0]: #"%s"のユーザー名を置き換える
			tech[0][0] = tech[0][0].replace("%s", self.player)
		if "%s" in tech[0][1]:
			tech[0][1] = tech[0][1].replace("%s", self.player)
		if "%s" in tech[1][0]:
			tech[1][0] = tech[1][0].replace("%s", self.player)
		if "%s" in tech[1][1]:
			tech[1][1] = tech[1][1].replace("%s", self.player)
			
		# ((22 * 威力 * 攻撃 / 防御 ) * 0.02 + 2) * 相性
		damage_nomal = ((22 * tech[2][0] * self.PROPS[me][4] / self.PROPS[ene][5]) * 0.02 + 2) * self.props_fig[ene_kind][me_kind]
		damage_spe = ((22 * tech[2][1] * self.PROPS[me][6] / self.PROPS[ene][7]) * 0.02 + 2) * self.props_fig[ene_kind][me_kind]
		damage_all[0].append(damage_nomal)
		damage_all[0].append(damage_spe)
		
		damage_nomal = ((22 * tech[3][0] * self.PROPS[ene][4] / self.PROPS[me][5]) * 0.02 + 2) * self.props_fig[me_kind][ene_kind]
		damage_spe = ((22 * tech[3][1] * self.PROPS[ene][6] / self.PROPS[me][7]) * 0.02 + 2) * self.props_fig[me_kind][ene_kind]
		damage_all[1].append(damage_nomal)
		damage_all[1].append(damage_spe)
		
		tech[2].append(self.tech_nomal[1][me_kind] / expect)# 命中率を設定
		tech[2].append(self.TECH_SPETI[1][me_kind] / expect)
		tech[3].append(self.tech_nomal[1][ene_kind] / expect)
		tech[3].append(self.TECH_SPETI[1][ene_kind] / expect)
		
		return data, damage_all, tech
		
	def comp(self): #コンプリートしたとき
		print('全てのイズモンを獲得した!')
		self.time.sleep(1)
		return
		
	def get(self, ene : int): #獲得処理
		prob = self.PROPS[ene][8] #獲得率
		if self.random.random() <= prob:
			before = sum(self.fellows) #獲"得前の数
			print(self.PROPS[ene][1], "を獲得した!")
			print("種族: %s HP: %d 攻撃: %d 防御: %d 特攻: %d 特防: %d" %
			(self.race[self.PROPS[ene][2]], self.PROPS[ene][3], self.PROPS[ene][4], self.PROPS[ene][5], self.PROPS[ene][6], self.PROPS[ene][7]))
			self.fellows[ene] = 1
			if sum(self.fellows) == self.iz_num and before == self.iz_num - 1: #初めてコンプリートした時のみ実行
				self.comp()
		else:
			self.pri("逃げられた…")
		return
		
	def turn_change(self, turn : int): #ターンを切り替える
		if turn == 1:
			return 0
		else:
			return 1
			
	def dic(self, ty : int = 1): #イズモン辞典を表示
		action = self.typing("何をするのじゃ？ 0:Myイズモン一覧を見る 1:種族値を見る",1 , 2)
		if action == 0:
			for i in range(self.iz_num):
				if self.fellows[i] == 1:
					print(self.PROPS[i][1])
					print("コード: %s 種族: %s HP: %d 攻撃: %d 防御: %d 特攻: %d 特防: %d" %
					(self.PROPS[i][0], self.race[self.PROPS[i][2]], self.PROPS[i][3], self.PROPS[i][4], self.PROPS[i][5], self.PROPS[i][6], self.PROPS[i][7]))
		else:
			while True:
				iz = self.typing("どのイズモンの種族値を見るのじゃ？",1, self.iz_num + 1) - 1 #コードと番地は1ずれている
				print(self.PROPS[iz][1])
				print("コード: %s 種族: %s HP: %d 攻撃: %d 防御: %d 特攻: %d 特防: %d" %
				(self.PROPS[iz][0], self.race[self.PROPS[iz][2]], self.PROPS[iz][3], self.PROPS[iz][4], self.PROPS[iz][5], self.PROPS[iz][6], self.PROPS[iz][7]))
				action = self.typing("どうするのじゃ？ 0:戻る 1:まだ見る", 1, 2)
				if action == 0:
					break
		if ty == 0:#バトル時以外
			action = self.typing("何をするのじゃ? 0:やめる 1:続ける 2:イズモン辞典を見る", 1, 3)
			if action == 0:
				return 0
			elif action == 1:
				return 1
			else:
				self.dic(0)
			return
		else:
			action = self.typing("どうするのじゃ? 0:バトルに戻る 1:まだ見る", 1, 2)
			if action == 0:
				return
			else:
				self.dic()
				
	def main(self):
		self.set_up()
		while True:
			enemy = self.random.randint(1, self.iz_num) - 1
			self.fight(enemy)
			ty = self.typing("続けますか? 0:やめる 1:続ける 2:イズモン辞典を見る", 1, 3)
			if ty == 1:
				continue
			elif ty == 2:
				res = self.dic(0)
				if res == 0:
					break
				else:
					continue
			else:
				break
		self.save()
		return

'''
2023年2月10日
19H あきた(コーディング)・鍋(設定考案)・みそ(企画)
CC : BY-NC-ND (表示-非営利-改変禁止)
'''
