from PIL import Image, ImageDraw
#  Image.MAX_IMAGE_PIXELS = None

def gen_map(X_R,Y_R,theta_R,X_G,Y_G,theta_G,State):
    hrobot = 35
    img_bg = Image.open("map_CFR2020.png")
    img_new = Image.new("RGBA", img_bg.size)
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
        img_fg = Image.open("Robot.png").convert('RGBA')
        img_fg_rotated = img_fg.rotate(theta_R, Image.NEAREST, True)
        img_new.paste(img_fg_rotated,(X_supleft, Y_supleft),img_fg_rotated)
        img_new.save("map_generated.png")
    if State == 1 : # Only Ghost
        X_supleft, Y_supleft = X_G - hrobot // 2, Y_G - hrobot // 2
        img_fg = Image.open("Ghost.png").convert('RGBA')
        img_fg_rotated = img_fg.rotate(theta_G, Image.NEAREST, True)
        img_new.paste(img_fg_rotated,(X_supleft, Y_supleft),img_fg_rotated)
        img_new.save("map_generated.png")
    if State == 2 : # Ghost & Robot
        X_supleft, Y_supleft = X_G - hrobot // 2, Y_G - hrobot // 2
        img_fg = Image.open("Ghost.png")
        img_fg_rotated = img_fg.rotate(theta_G, Image.BICUBIC, True)
        img_new.paste(img_fg_rotated, (X_supleft, Y_supleft),img_fg_rotated)
        X_supleft, Y_supleft = X_R - hrobot // 2, Y_R - hrobot // 2
        img_fg = Image.open("Robot.png")
        img_fg_rotated = img_fg.rotate(theta_R, Image.BICUBIC, True)
        img_new.paste(img_fg_rotated,(X_supleft, Y_supleft),img_fg_rotated)
        image_draw = Image.new("RGBA", img_bg.size)
        draw_img = ImageDraw.Draw(image_draw)
        draw_img.line([(X_G, Y_G), (X_R, Y_R)], (44, 240, 7), 3)
        img_new.paste(image_draw, image_draw)
        img_new.save("map_generated.png")
