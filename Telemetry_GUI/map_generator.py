from PIL import Image, ImageDraw
#  Image.MAX_IMAGE_PIXELS = None

def gen_map(X_R,Y_R,theta_R,X_G,Y_G,theta_G,State):
    hrobot = 70
    img_bg = Image.open("map_CFR2020.png")
    fac = 100
    X_R = int(X_R*fac)
    Y_R = int(Y_R *fac)
    theta_R = int(theta_R*fac)
    X_G = int(X_G*fac)
    Y_G = int(Y_G*fac)
    theta_G = int(theta_G*fac)
    #  width, height = 895, 597
    if State == 0 : # Only Robot
        X_supleft, Y_supleft = X_R - hrobot // 2, Y_R - hrobot // 2
        img_fg = Image.open("Bot_UpperView_Cut_NoBg.png")
        img_fg = img_fg.resize((hrobot,hrobot))
        img_fg_rotated = img_fg.rotate(theta_R)
        img_bg.paste(img_fg_rotated,(X_supleft, Y_supleft),img_fg_rotated)
        img_bg.save("map_generated.png")
    if State == 1 : # Only Ghost
        X_supleft, Y_supleft = X_G - hrobot // 2, Y_G - hrobot // 2
        img_fg = Image.open("Bot_UpperView_Cut_NoBg_Filter_Ghost.png")
        img_fg = img_fg.resize((hrobot, hrobot))
        img_fg_rotated = img_fg.rotate(theta_G)
        img_bg.paste(img_fg_rotated, (X_supleft, Y_supleft), img_fg_rotated)
        img_bg.save("map_generated.png")
    if State == 2 : # Robot and Ghost
        image_draw = Image.new("RGBA", img_bg.size)
        draw_img = ImageDraw.Draw(image_draw)
        draw_img.line([(X_G, X_G), (X_R, Y_R)], (44,240,7) , 3)
        img_bg.paste(image_draw, image_draw)
        X_supleft, Y_supleft = X_G - hrobot // 2, Y_G - hrobot // 2
        img_fg = Image.open("Bot_UpperView_Cut_NoBg_Filter_Ghost.png")
        img_fg = img_fg.resize((hrobot, hrobot))
        img_fg_rotated = img_fg.rotate(theta_G)
        img_bg.paste(img_fg_rotated, (X_supleft, Y_supleft), img_fg_rotated)
        X_supleft, Y_supleft = X_R - hrobot // 2, Y_R - hrobot // 2
        img_fg = Image.open("Bot_UpperView_Cut_NoBg.png")
        img_fg = img_fg.resize((hrobot, hrobot))
        img_fg_rotated = img_fg.rotate(theta_R)
        img_bg.paste(img_fg_rotated, (X_supleft, Y_supleft), img_fg_rotated)
        img_bg.save("map_generated.png")
