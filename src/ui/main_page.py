import flet as ft
import os
from utils.config import *
from services.genetic_functions import *

def main(page: ft.Page):
    page.title = "🛡️ Evolução de Criaturas - Algoritmo Genético"
    page.scroll = "auto"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 0
    
    background_path = os.path.join(os.getcwd(), "assets", "background.png")
    has_background = os.path.exists(background_path)
    
    if has_background:
        page.bgcolor = ft.Colors.TRANSPARENT
        background_image = "/background.png"
    else:
        page.bgcolor = "#1a0f0a"
        background_image = None

    titulo = ft.Container(
        content=ft.Column([
            ft.Text(
                "⚔️ TAVERNA DA EVOLUÇÃO ⚔️",
                size=36,
                weight=ft.FontWeight.BOLD,
                color="#FFD700",
                text_align=ft.TextAlign.CENTER,
                font_family="serif",
            ),
            ft.Text(
                "~ Algoritmo Genético dos Heróis ~",
                size=16,
                color="#D4AF37",
                text_align=ft.TextAlign.CENTER,
                italic=True,
                font_family="serif",
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
        padding=20,
        bgcolor=ft.Colors.with_opacity(0.85, "#2d1810"),
        border=ft.border.all(3, "#8B4513"),
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        ),
    )

    lbl_geracao = ft.Text("Geração: 0", color="#FFE4B5", size=18, weight=ft.FontWeight.BOLD, font_family="serif")
    lbl_melhor = ft.Text("Melhor Herói: 0", color="#90EE90", size=18, weight=ft.FontWeight.BOLD, font_family="serif")
    
    info_panel = ft.Container(
        content=ft.Row([
            ft.Container(
                content=lbl_geracao,
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.8, "#3d2817"),
                border=ft.border.all(2, "#CD853F"),
                border_radius=8,
            ),
            ft.Container(
                content=lbl_melhor,
                padding=15,
                bgcolor=ft.Colors.with_opacity(0.8, "#3d2817"),
                border=ft.border.all(2, "#CD853F"),
                border_radius=8,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=20),
        margin=ft.margin.only(top=20, bottom=10),
    )
    
    area_personagens = ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=15)

    populacao = inicializar_populacao()
    geracao = 0
    historico_melhores = []
    historico_por_raca = {raca: [] for raca in SPRITES_POR_TIPO.keys()}

    chart_geral = ft.LineChart(
        data_series=[],
        border=ft.border.all(2, "#8B4513"),
        height=180,
        width=280,
        bgcolor=ft.Colors.with_opacity(0.85, "#2d1810"),
        horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.with_opacity(0.3, "#CD853F")),
        vertical_grid_lines=ft.ChartGridLines(color=ft.Colors.with_opacity(0.3, "#CD853F")),
        animate=500,
    )
    
    charts_racas = {}
    cores_racas = {
        "Templário": "#FFD700",
        "Clérigo": "#87CEEB",
        "Dragão": "#FF4500",
        "Guerreiro": "#CD853F",
        "Mago": "#9370DB"
    }
    
    for raca in SPRITES_POR_TIPO.keys():
        charts_racas[raca] = ft.LineChart(
            data_series=[],
            border=ft.border.all(2, "#8B4513"),
            height=180,
            width=280,
            bgcolor=ft.Colors.with_opacity(0.85, "#2d1810"),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.with_opacity(0.3, "#CD853F")),
            vertical_grid_lines=ft.ChartGridLines(color=ft.Colors.with_opacity(0.3, "#CD853F")),
            animate=500,
        )
    
    chart_geral_container = ft.Container(
        content=ft.Column([
            ft.Text("📊 Evolução Geral", size=14, weight=ft.FontWeight.BOLD, color="#FFD700", font_family="serif"),
            chart_geral,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
        padding=10,
        border=ft.border.all(3, "#8B4513"),
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.9, "#1a0f0a"),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
        ),
    )
    
    chart_raca_containers = []
    for raca, chart in charts_racas.items():
        container = ft.Container(
            content=ft.Column([
                ft.Text(f"⚔️ {raca}", size=14, weight=ft.FontWeight.BOLD, color=cores_racas[raca], font_family="serif"),
                chart,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            padding=10,
            border=ft.border.all(3, "#8B4513"),
            border_radius=10,
            bgcolor=ft.Colors.with_opacity(0.9, "#1a0f0a"),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            ),
        )
        chart_raca_containers.append(container)
    
    area_graficos = ft.Column([
        ft.Row([chart_geral_container] + chart_raca_containers[:2], 
               alignment=ft.MainAxisAlignment.CENTER, spacing=15, wrap=True),
        ft.Row(chart_raca_containers[2:], 
               alignment=ft.MainAxisAlignment.CENTER, spacing=15, wrap=True),
    ], spacing=15)

    def criar_barra_atributo(icone, valor, cor, max_valor=100):
        """Cria uma barra de atributo estilo RPG"""
        porcentagem = (valor / max_valor) * 100
        return ft.Container(
            content=ft.Stack([
                ft.Container(
                    width=100,
                    height=8,
                    bgcolor=ft.Colors.with_opacity(0.3, "#000000"),
                    border_radius=4,
                ),
                ft.Container(
                    width=porcentagem,
                    height=8,
                    bgcolor=cor,
                    border_radius=4,
                ),
            ]),
            margin=ft.margin.only(top=2, bottom=2),
        )

    def atualizar_tela():
        area_personagens.controls.clear()
        
        ids_vistos = set()
        criaturas_unicas = []
        
        for criatura in populacao:
            if criatura.id not in ids_vistos:
                ids_vistos.add(criatura.id)
                criaturas_unicas.append(criatura)
        
        for criatura in criaturas_unicas:
            criatura.calcular_fitness()

            card = ft.Container(
                content=ft.Column([
                    ft.Container(
                        height=2,
                        bgcolor="#D4AF37",
                        border_radius=ft.border_radius.only(top_left=10, top_right=10),
                    ),
                    
                    ft.Container(
                        content=ft.Image(
                            src=f"/{criatura.sprite_path}",
                            width=100,
                            height=100,
                            fit=ft.ImageFit.CONTAIN,
                            error_content=ft.Container(
                                content=ft.Text("⚔️", size=50),
                                bgcolor=ft.Colors.with_opacity(0.3, "#8B0000"),
                            )
                        ),
                        bgcolor=ft.Colors.with_opacity(0.2, "#000000"),
                        padding=10,
                        border=ft.border.all(2, "#8B4513"),
                        border_radius=8,
                        margin=5,
                    ),
                    
                    ft.Container(
                        content=ft.Text(
                            f"⚜️ {criatura.tipo} ⚜️",
                            color="#FFD700",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            font_family="serif",
                        ),
                        bgcolor=ft.Colors.with_opacity(0.6, "#8B4513"),
                        padding=5,
                        border_radius=5,
                        margin=5,
                    ),
                    
                    ft.Container(
                        content=ft.Text(
                            f"⭐ Poder: {criatura.fitness:.0f}",
                            color="#FFE4B5",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=5,
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("⚔️", size=12),
                                criar_barra_atributo("⚔️", criatura.forca, "#FF6B6B"),
                                ft.Text(f"{criatura.forca:.0f}", size=10, color="#FFE4B5"),
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                            
                            ft.Row([
                                ft.Text("🏃", size=12),
                                criar_barra_atributo("🏃", criatura.agilidade, "#4ECDC4"),
                                ft.Text(f"{criatura.agilidade:.0f}", size=10, color="#FFE4B5"),
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                            
                            ft.Row([
                                ft.Text("📖", size=12),
                                criar_barra_atributo("📖", criatura.inteligencia, "#95E1D3"),
                                ft.Text(f"{criatura.inteligencia:.0f}", size=10, color="#FFE4B5"),
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                            
                            ft.Row([
                                ft.Text("❤️", size=12),
                                criar_barra_atributo("❤️", criatura.vitalidade, "#F38181"),
                                ft.Text(f"{criatura.vitalidade:.0f}", size=10, color="#FFE4B5"),
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                            
                            ft.Row([
                                ft.Text("🙏", size=12),
                                criar_barra_atributo("🙏", criatura.fe, "#F8B500"),
                                ft.Text(f"{criatura.fe:.0f}", size=10, color="#FFE4B5"),
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                            
                            ft.Row([
                                ft.Text("💫", size=12),
                                criar_barra_atributo("💫", criatura.carisma, "#AA96DA"),
                                ft.Text(f"{criatura.carisma:.0f}", size=10, color="#FFE4B5"),
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                        ], spacing=3),
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(0.3, "#1a0f0a"),
                        border_radius=5,
                        margin=5,
                    ),
                    
                    ft.Container(
                        height=2,
                        bgcolor="#8B4513",
                        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
                    ),
                ], alignment=ft.MainAxisAlignment.START, spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=140,
                bgcolor=ft.Colors.with_opacity(0.95, "#2d1810"),
                border=ft.border.all(3, "#8B4513"),
                border_radius=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.Colors.with_opacity(0.6, "#000000"),
                    offset=ft.Offset(0, 5),
                ),
                animate_scale=ft.Animation(400, ft.AnimationCurve.EASE_OUT_BACK),
                on_hover=lambda e: setattr(e.control, "scale", 1.05 if e.data == "true" else 1.0)
            )
            area_personagens.controls.append(card)

        lbl_geracao.value = f"📜 Geração: {geracao}"
        melhor = max(populacao, key=lambda c: c.fitness)
        lbl_melhor.value = f"🏆 Melhor Herói: {melhor.fitness:.0f} ({melhor.tipo})"

        historico_melhores.append(melhor.fitness)
        chart_geral.data_series = [
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(i, f) for i, f in enumerate(historico_melhores)],
                stroke_width=3,
                color="#FFD700",
                curved=True,
                stroke_cap_round=True,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.Colors.with_opacity(0.5, "#FFD700"),
                ),
            )
        ]
        
        for raca in SPRITES_POR_TIPO.keys():
            criaturas_raca = [c for c in populacao if c.tipo == raca]
            if criaturas_raca:
                melhor_raca = max(criaturas_raca, key=lambda c: c.fitness)
                historico_por_raca[raca].append(melhor_raca.fitness)
            else:
                if historico_por_raca[raca]:
                    historico_por_raca[raca].append(historico_por_raca[raca][-1])
                else:
                    historico_por_raca[raca].append(0)
            
            charts_racas[raca].data_series = [
                ft.LineChartData(
                    data_points=[ft.LineChartDataPoint(i, f) for i, f in enumerate(historico_por_raca[raca])],
                    stroke_width=3,
                    color=cores_racas[raca],
                    curved=True,
                    stroke_cap_round=True,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.with_opacity(0.5, cores_racas[raca]),
                    ),
                )
            ]
        
        page.update()

    def evoluir_click(e):
        nonlocal populacao, geracao
        if geracao < NUM_GERACOES:
            populacao = nova_geracao(populacao)
            geracao += 1
            atualizar_tela()
        else:
            lbl_geracao.value = "🏁 A lenda está completa!"
            page.update()

    botao_evoluir = ft.Container(
        content=ft.Text(
            "⚔️ EVOLUIR GERAÇÃO ⚔️",
            size=18,
            weight=ft.FontWeight.BOLD,
            color="#FFFFFF",
            text_align=ft.TextAlign.CENTER,
        ),
        on_click=evoluir_click,
        bgcolor="#8B4513",
        padding=15,
        border=ft.border.all(3, "#D4AF37"),
        border_radius=10,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.5, "#000000"),
            offset=ft.Offset(0, 4),
        ),
        animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        on_hover=lambda e: setattr(e.control, "scale", 1.05 if e.data == "true" else 1.0),
        margin=20,
    )

    main_content = ft.Container(
        content=ft.Column([
            titulo,
            info_panel,
            area_graficos,
            botao_evoluir,
            ft.Container(height=10), 
            area_personagens
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, scroll=ft.ScrollMode.AUTO),
        padding=20,
        image=background_image if has_background else None,
        expand=True,
    )

    page.add(main_content)
    atualizar_tela()