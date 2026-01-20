import asyncio
import pygame
import sys
import pathlib
import base64

async def main():
    pygame.init()

    score = 0
    multiplier = 1
    used_codes = []

    def xor_data(data):
        return "".join(chr(ord(c) ^ (i % 255)) for i, c in enumerate(data))

    try:
        font_style = pygame.font.Font("Other/font.ttf", 74)
        button_font = pygame.font.Font("Other/font.ttf", 30)
        small_font = pygame.font.Font("Other/font.ttf", 24)
    except:
        font_style = pygame.font.SysFont("Arial", 74)
        button_font = pygame.font.SysFont("Arial", 30)
        small_font = pygame.font.SysFont("Arial", 24)

    data_file = pathlib.Path("data")
    score_file = pathlib.Path("score")
    show_cutscenes = not data_file.exists()

    if score_file.exists():
        try:
            with open("score", "r") as f:
                encoded_content = f.read()
                decoded_bytes = base64.b64decode(encoded_content)
                xor_decoded = decoded_bytes.decode("utf-8")
                content = xor_data(xor_decoded)
                data_parts = content.split("|")
                for part in data_parts:
                    if "score=" in part:
                        score = int(part.split("=")[1])
                    elif "mult=" in part:
                        multiplier = int(part.split("=")[1])
                    elif "used=" in part:
                        used_codes = part.split("=")[1].split(",")
                        if used_codes == ['']:
                            used_codes = []
        except:
            score = 0
            multiplier = 1
            used_codes = []

    if show_cutscenes:
        try:
            with open("data", "w") as f:
                f.write("played")
        except:
            pass

    screen = pygame.display.set_mode((1280, 720))
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    if show_cutscenes:
        cutscene_paths = [
            "Cutscenes/cutscene1.png",
            "Cutscenes/cutscene2.png",
            "Cutscenes/cutscene3.png"
        ]
        
        current_scene = 0
        viewing_cutscenes = True
        
        while viewing_cutscenes:
            try:
                scene_image = pygame.image.load(cutscene_paths[current_scene]).convert()
                scene_image = pygame.transform.smoothscale(scene_image, (WIDTH, HEIGHT))
                scene_rect = scene_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            except:
                viewing_cutscenes = False
                break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        current_scene += 1
                        if current_scene >= len(cutscene_paths):
                            viewing_cutscenes = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        current_scene += 1
                        if current_scene >= len(cutscene_paths):
                            viewing_cutscenes = False
            
            if viewing_cutscenes:
                screen.fill("black")
                screen.blit(scene_image, scene_rect)
                pygame.display.flip()
                await asyncio.sleep(0)
                clock.tick(60)

    def load_background(path):
        try:
            img = pygame.image.load(path).convert()
            img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
            return img
        except:
            fallback = pygame.Surface((WIDTH, HEIGHT))
            fallback.fill((100, 100, 100))
            return fallback

    def save_data(s, m, u):
        codes_str = ",".join(u)
        raw_data = f"score={s}|mult={m}|used={codes_str}"
        xored_data = xor_data(raw_data)
        encoded_data = base64.b64encode(xored_data.encode("utf-8")).decode("utf-8")
        with open("score", "w") as file:
            file.write(encoded_data)

    jobs_config = [
        {"cost": 100, "mult": 2, "name": "J*b 1"},
        {"cost": 350, "mult": 3, "name": "J*b 2"},
        {"cost": 1000, "mult": 5, "name": "J*b 3"},
        {"cost": 5000, "mult": 8, "name": "J*b 4"},
        {"cost": 8000, "mult": 10, "name": "J*b 5"},
        {"cost": 10000, "mult": 12, "name": "J*b 6"}
    ]

    if score < 100:
        current_level = 1
        bg_path = "Backgrounds/level1.png"
    elif score < 400:
        current_level = 2
        bg_path = "Backgrounds/level2.png"
    elif score < 2000:
        current_level = 3
        bg_path = "Backgrounds/level3.png"
    else:
        current_level = 4
        bg_path = "Backgrounds/level4.png"

    image = load_background(bg_path)
    image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    label = font_style.render(str(score), True, (0, 0, 0))
    label_rect = label.get_rect(centerx=WIDTH // 2, top=20)

    upgrade_button_rect = pygame.Rect(WIDTH - 350, 100, 320, 80)
    codes_button_rect = pygame.Rect(WIDTH - 350, 200, 320, 80)

    codes_tab_active = False
    code_input_text = ""
    code_feedback = ""
    code_feedback_timer = 0

    level_display_start = pygame.time.get_ticks()
    level_display_duration = 3000
    current_level_text = f"Level {current_level}"

    while True:
        current_ticks = pygame.time.get_ticks()
        is_level_showing = current_ticks - level_display_start < level_display_duration

        next_job_index = -1
        for i, job in enumerate(jobs_config):
            if multiplier < job["mult"]:
                next_job_index = i
                break

        if score >= 2000 and current_level == 3:
            current_level = 4
            image = load_background("Backgrounds/level4.png")
            image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            current_level_text = "Level 4"
            level_display_start = pygame.time.get_ticks()
        elif score >= 400 and current_level == 2:
            current_level = 3
            image = load_background("Backgrounds/level3.png")
            image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            current_level_text = "Level 3"
            level_display_start = pygame.time.get_ticks()
        elif score >= 100 and current_level == 1:
            current_level = 2
            image = load_background("Backgrounds/level2.png")
            image_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            current_level_text = "Level 2"
            level_display_start = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if codes_tab_active:
                if event.type == pygame.TEXTINPUT:
                    if len(code_input_text) < 20:
                        code_input_text += event.text
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        code_input_text = code_input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        user_input_encoded = base64.b64encode(code_input_text.lower().strip().encode("utf-8")).decode("utf-8")
                        if user_input_encoded in used_codes:
                            code_feedback = "Already Used!"
                        elif user_input_encoded == "Z3Jhc3N0b3VjaGVy":
                            multiplier *= 2
                            code_feedback = "Multiplier Doubled!"
                            used_codes.append(user_input_encoded)
                        elif user_input_encoded == "emVhY2xl":
                            multiplier += 3
                            code_feedback = "Multiplier +3!"
                            used_codes.append(user_input_encoded)
                        elif user_input_encoded == "emh2YW55YWh5YQ==":
                            multiplier += 10
                            code_feedback = "Multiplier +10!"
                            used_codes.append(user_input_encoded)
                        elif user_input_encoded == "NmY0bGlmZQ==":
                            multiplier *= 2
                            code_feedback = "Multiplier Doubled!"
                            used_codes.append(user_input_encoded)
                        else:
                            code_feedback = "Invalid Code"
                        
                        code_input_text = ""
                        code_feedback_timer = pygame.time.get_ticks()
                        save_data(score, multiplier, used_codes)
                    elif event.key == pygame.K_ESCAPE:
                        codes_tab_active = False
                        pygame.key.stop_text_input()

            if event.type == pygame.KEYDOWN and not codes_tab_active:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if codes_tab_active:
                        tab_rect = pygame.Rect(0, 0, 400, 250)
                        tab_rect.center = (WIDTH // 2, HEIGHT // 2)
                        if not tab_rect.collidepoint(event.pos):
                            codes_tab_active = False
                            pygame.key.stop_text_input()
                        else:
                            close_clickable_rect = pygame.Rect(tab_rect.right - 50, tab_rect.top, 50, 50)
                            if close_clickable_rect.collidepoint(event.pos):
                                codes_tab_active = False
                                pygame.key.stop_text_input()
                    else:
                        if codes_button_rect.collidepoint(event.pos):
                            codes_tab_active = True
                            code_feedback = ""
                            code_input_text = ""
                            pygame.key.start_text_input()
                        elif upgrade_button_rect.collidepoint(event.pos) and not is_level_showing:
                            if next_job_index != -1:
                                target_job = jobs_config[next_job_index]
                                if score >= target_job["cost"]:
                                    multiplier = target_job["mult"]
                                    save_data(score, multiplier, used_codes)
                        elif not is_level_showing:
                            score += (1 * multiplier)
                            label = font_style.render(str(score), True, (0, 0, 0))
                            label_rect = label.get_rect(centerx=WIDTH // 2, top=20)
                            save_data(score, multiplier, used_codes)
                        
        screen.fill("white")
        screen.blit(image, image_rect)
        screen.blit(label, label_rect)

        if next_job_index != -1:
            current_cost = jobs_config[next_job_index]["cost"]
            job_name = jobs_config[next_job_index]["name"]
            if score >= current_cost:
                button_color = (0, 200, 0)
                upgrade_text = f"Unlock {job_name}"
            else:
                button_color = (130, 130, 130)
                upgrade_text = f"{job_name} (Needs: {current_cost})"
        else:
            button_color = (255, 215, 0)
            upgrade_text = "All J*bs Obtained"
        
        pygame.draw.rect(screen, button_color, upgrade_button_rect, border_radius=15)
        button_label = button_font.render(upgrade_text, True, (255, 255, 255))
        button_label_rect = button_label.get_rect(center=upgrade_button_rect.center)
        screen.blit(button_label, button_label_rect)

        pygame.draw.rect(screen, (70, 70, 200), codes_button_rect, border_radius=15)
        codes_label = button_font.render("Codes", True, (255, 255, 255))
        codes_label_rect = codes_label.get_rect(center=codes_button_rect.center)
        screen.blit(codes_label, codes_label_rect)

        if codes_tab_active:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            tab_rect = pygame.Rect(0, 0, 400, 250)
            tab_rect.center = (WIDTH // 2, HEIGHT // 2)
            pygame.draw.rect(screen, (240, 240, 240), tab_rect, border_radius=20)
            pygame.draw.rect(screen, (0, 0, 0), tab_rect, 3, border_radius=20)
            
            title = button_font.render("Enter Secret Code", True, (0, 0, 0))
            screen.blit(title, (tab_rect.x + 50, tab_rect.y + 30))
            
            input_box = pygame.Rect(tab_rect.x + 50, tab_rect.y + 100, 300, 50)
            pygame.draw.rect(screen, (255, 255, 255), input_box)
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
            
            text_surf = small_font.render(code_input_text, True, (0, 0, 0))
            screen.blit(text_surf, (input_box.x + 10, input_box.y + 12))
            
            if code_feedback and pygame.time.get_ticks() - code_feedback_timer < 2000:
                feedback_surf = small_font.render(code_feedback, True, (200, 0, 0))
                screen.blit(feedback_surf, (tab_rect.x + 50, tab_rect.y + 170))

            close_text = small_font.render("X", True, (200, 0, 0))
            close_btn_rect = close_text.get_rect(topright=(tab_rect.right - 15, tab_rect.top + 10))
            screen.blit(close_text, close_btn_rect)

        if is_level_showing:
            overlay_text = font_style.render(current_level_text, True, (255, 0, 0))
            overlay_rect = overlay_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(overlay_text, overlay_rect)

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

asyncio.run(main())
