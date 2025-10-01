# ENDPOINTS PARA APP MÓVIL - CONDOMINIUM
# =====================================
# Enfoque: RESIDENTES + GUARDIAS (Pagos + Monitoreo)

"""
📱 ANÁLISIS DE ENDPOINTS PARA APP MÓVIL
=======================================

La app móvil tendrá 2 perfiles principales:
1. 👥 RESIDENTES: Pagos, reservas, avisos, perfil
2. 👮 GUARDIAS: Monitoreo, accesos, seguridad, eventos

🎯 FUNCIONALIDADES CLAVE:
- Pagos de cuotas y conceptos
- Monitoreo de accesos en tiempo real  
- Reservas de áreas comunes
- Comunicación (avisos)
- Reconocimiento facial para acceso
- Control de vehículos
- Alertas de seguridad
"""

def endpoints_para_app_movil():
    
    endpoints = {
        
        # =================================================================
        # 🔐 AUTENTICACIÓN (AMBOS PERFILES)
        # =================================================================
        "AUTENTICACION": {
            "POST /ad/auth/login": {
                "descripcion": "Login para residentes y guardias",
                "body": {
                    "correo": "residente@email.com | guardia@email.com", 
                    "password": "password123"
                },
                "respuesta": {
                    "codigo": 0,
                    "mensaje": "OK",
                    "token": "jwt_token_here",
                    "usuario_id": 1,
                    "perfil": "RESIDENTE | GUARDIA | ADMIN"
                },
                "uso_app": "Pantalla de login, guardar token en storage seguro"
            },
            
            "GET /ad/usuarios/{usuario_id}/": {
                "descripcion": "Obtener perfil del usuario logueado",
                "headers": {"Authorization": "Bearer jwt_token"},
                "respuesta": {
                    "id": 1,
                    "nombre": "Juan Pérez",
                    "correo": "juan@email.com",
                    "foto": "url_foto",
                    "roles": ["RESIDENTE"]
                },
                "uso_app": "Mostrar datos en perfil de usuario"
            }
        },

        # =================================================================
        # 👥 ENDPOINTS PARA RESIDENTES
        # =================================================================
        "RESIDENTES_PAGOS": {
            "GET /cn/cuotas/?residente_id={id}": {
                "descripcion": "Cuotas del residente (pendientes/pagadas)",
                "query_params": {
                    "residente_id": "ID del residente",
                    "estado": "PENDIENTE | PAGADO | VENCIDO",
                    "fecha_desde": "2024-01-01",
                    "fecha_hasta": "2024-12-31"
                },
                "respuesta": [
                    {
                        "id": 1,
                        "concepto": "Gas Domiciliario",
                        "monto": 50.00,
                        "fecha_vencimiento": "2024-11-30",
                        "estado": "PENDIENTE",
                        "dias_vencido": 0
                    }
                ],
                "uso_app": "📋 Pantalla principal: Lista de cuotas pendientes"
            },

            "GET /cn/conceptos-precio/": {
                "descripcion": "Conceptos disponibles para pago",
                "respuesta": [
                    {
                        "id": 1,
                        "nombre": "Gas Domiciliario", 
                        "monto": 50.00,
                        "tipo": "SERVICIO",
                        "vigente": True
                    }
                ],
                "uso_app": "💰 Pantalla de pagos: Seleccionar concepto"
            },

            "POST /cn/cuotas/{cuota_id}/pagar/": {
                "descripcion": "⚠️ ENDPOINT A CREAR - Registrar pago de cuota",
                "body": {
                    "forma_pago_id": 1,
                    "monto": 50.00,
                    "comprobante": "base64_image_or_url"
                },
                "respuesta": {
                    "codigo": 0,
                    "mensaje": "Pago registrado exitosamente",
                    "cuota_id": 1,
                    "estado": "PAGADO"
                },
                "uso_app": "💳 Registrar pago y subir comprobante"
            },

            "GET /cn/formas-pago/": {
                "descripcion": "Métodos de pago disponibles",
                "respuesta": [
                    {
                        "id": 1,
                        "nombre": "Transferencia Bancaria",
                        "descripcion": "Banco XYZ - Cuenta 123456"
                    }
                ],
                "uso_app": "💳 Selector de método de pago"
            }
        },

        "RESIDENTES_SERVICIOS": {
            "GET /ad/areas-comunes/": {
                "descripcion": "Áreas disponibles para reserva",
                "respuesta": [
                    {
                        "id": 1,
                        "nombre": "Salón de Fiestas",
                        "capacidad": 50,
                        "tarifa": 100.00,
                        "disponible": True
                    }
                ],
                "uso_app": "🏊 Lista de áreas para reservar"
            },

            "GET /ad/reservas-area/?residente_id={id}": {
                "descripcion": "Reservas del residente",
                "respuesta": [
                    {
                        "id": 1,
                        "area": "Salón de Fiestas",
                        "fecha_evento": "2024-12-15",
                        "estado": "CONFIRMADO"
                    }
                ],
                "uso_app": "📅 Mis reservas"
            },

            "POST /ad/reservas-area/": {
                "descripcion": "Crear nueva reserva",
                "body": {
                    "area_id": 1,
                    "residente_id": 1,
                    "fecha_evento": "2024-12-15",
                    "observaciones": "Cumpleaños infantil"
                },
                "uso_app": "➕ Nueva reserva"
            },

            "GET /ad/avisos/": {
                "descripcion": "Avisos para residentes",
                "query_params": {"activos": "true"},
                "respuesta": [
                    {
                        "id": 1,
                        "titulo": "Corte de agua programado",
                        "contenido": "El día 15/11 habrá corte...",
                        "fecha_publicacion": "2024-11-01",
                        "vigente_hasta": "2024-11-15"
                    }
                ],
                "uso_app": "📢 Pantalla de comunicados"
            },

            "GET /ad/residentes/mis-datos/{usuario_id}/": {
                "descripcion": "⚠️ ENDPOINT A CREAR - Datos del residente",
                "respuesta": {
                    "id": 1,
                    "nombres": "Juan Carlos",
                    "unidad": "Torre A - Apt 101",
                    "vehiculos": [
                        {"placa": "ABC123", "modelo": "Toyota Corolla"}
                    ],
                    "telefono": "+591 7xxxxxxx"
                },
                "uso_app": "👤 Perfil del residente"
            }
        },

        # =================================================================
        # 👮 ENDPOINTS PARA GUARDIAS  
        # =================================================================
        "GUARDIAS_MONITOREO": {
            "POST /api/ai/escanear-rostro/": {
                "descripcion": "Reconocimiento facial para acceso",
                "body": "multipart/form-data con 'image'",
                "respuesta": {
                    "matched": True,
                    "resident": "Juan Pérez",
                    "confidence": 95.5,
                    "unidad": "Torre A - 101"
                },
                "uso_app": "📸 Cámara para escanear rostros"
            },

            "POST /api/ai/escanear-placa/": {
                "descripcion": "Reconocimiento de placas vehiculares",
                "body": "multipart/form-data con 'image'", 
                "respuesta": {
                    "placa_detectada": "ABC123",
                    "confidence": 89.2,
                    "vehiculo_registrado": True,
                    "propietario": "Juan Pérez"
                },
                "uso_app": "🚗 Cámara para escanear placas"
            },

            "GET /api/ai/eventos-acceso/": {
                "descripcion": "⚠️ ENDPOINT A CREAR - Historial de accesos",
                "query_params": {
                    "fecha": "2024-11-01",
                    "tipo": "ROSTRO | PLACA",
                    "resultado": "PERMITIDO | DENEGADO"
                },
                "respuesta": [
                    {
                        "id": 1,
                        "timestamp": "2024-11-01 14:30:00",
                        "tipo": "ROSTRO",
                        "resultado": "PERMITIDO", 
                        "residente": "Juan Pérez",
                        "confidence": 95.5,
                        "imagen": "url_imagen"
                    }
                ],
                "uso_app": "📊 Log de eventos de acceso"
            },

            "GET /ad/residentes/": {
                "descripcion": "Lista de residentes para verificación",
                "query_params": {"activos": "true"},
                "respuesta": [
                    {
                        "id": 1,
                        "nombres": "Juan Pérez",
                        "unidad": "Torre A - 101",
                        "foto": "url_foto",
                        "telefono": "+591 7xxxxxxx"
                    }
                ],
                "uso_app": "👥 Directorio de residentes"
            },

            "GET /ad/vehiculos/": {
                "descripcion": "Vehículos registrados",
                "respuesta": [
                    {
                        "id": 1,
                        "placa": "ABC123",
                        "marca": "Toyota",
                        "modelo": "Corolla",
                        "propietario": "Juan Pérez",
                        "unidad": "Torre A - 101"
                    }
                ],
                "uso_app": "🚗 Directorio de vehículos"
            },

            "POST /api/ai/registrar-evento-manual/": {
                "descripcion": "⚠️ ENDPOINT A CREAR - Registrar evento manual",
                "body": {
                    "tipo": "VISITA | DELIVERY | MANTENIMIENTO",
                    "descripcion": "Visita familiar",
                    "residente_id": 1,
                    "visitante_nombre": "María García",
                    "documento": "12345678"
                },
                "uso_app": "✍️ Registro manual de visitas"
            }
        },

        # =================================================================
        # 🚨 ENDPOINTS PARA ALERTAS Y NOTIFICACIONES
        # =================================================================
        "ALERTAS_NOTIFICACIONES": {
            "GET /api/ai/eventos-sospechosos/": {
                "descripcion": "⚠️ ENDPOINT A CREAR - Eventos sospechosos detectados",
                "query_params": {"fecha_desde": "2024-11-01"},
                "respuesta": [
                    {
                        "id": 1,
                        "timestamp": "2024-11-01 02:30:00",
                        "tipo_comportamiento": "PERSONA_SOSPECHOSA",
                        "confidence": 87.3,
                        "ubicacion": "Entrada principal",
                        "imagen": "url_imagen",
                        "atendido": False
                    }
                ],
                "uso_app": "🚨 Alertas para guardias"
            },

            "PUT /api/ai/eventos-sospechosos/{id}/atender/": {
                "descripcion": "⚠️ ENDPOINT A CREAR - Marcar alerta como atendida",
                "body": {
                    "guardia_id": 1,
                    "observaciones": "Revisado, todo normal"
                },
                "uso_app": "✅ Marcar alerta como resuelta"
            },

            "POST /notificaciones/push/": {
                "descripcion": "⚠️ ENDPOINT A CREAR - Enviar notificación push",
                "body": {
                    "destinatarios": ["GUARDIAS | RESIDENTES | ADMIN"],
                    "titulo": "Alerta de seguridad",
                    "mensaje": "Comportamiento sospechoso detectado",
                    "tipo": "URGENTE | INFO"
                },
                "uso_app": "📱 Sistema de notificaciones"
            }
        },

        # =================================================================
        # 📊 ENDPOINTS PARA DASHBOARDS
        # =================================================================
        "DASHBOARDS": {
            "GET /api/dashboard/residente/{residente_id}/": {
                "descripcion": "⚠️ ENDPOINT A CREAR - Dashboard del residente",
                "respuesta": {
                    "cuotas_pendientes": 2,
                    "monto_total_pendiente": 150.00,
                    "proxima_cuota_vence": "2024-11-30",
                    "reservas_activas": 1,
                    "avisos_sin_leer": 3
                },
                "uso_app": "📊 Pantalla principal del residente"
            },

            "GET /api/dashboard/guardia/": {
                "descripcion": "⚠️ ENDPOINT A CREAR - Dashboard del guardia",
                "respuesta": {
                    "accesos_hoy": 45,
                    "visitantes_registrados": 12,
                    "alertas_pendientes": 2,
                    "vehiculos_ingresados": 23,
                    "ultima_actividad": "2024-11-01 15:45:00"
                },
                "uso_app": "📊 Pantalla principal del guardia"
            }
        }
    }
    
    return endpoints

def endpoints_faltantes_por_crear():
    """
    ⚠️ ENDPOINTS QUE NECESITAS CREAR PARA LA APP
    """
    
    faltantes = [
        {
            "endpoint": "POST /cn/cuotas/{id}/pagar/",
            "prioridad": "🔴 ALTA",
            "razon": "Función principal de residentes - registrar pagos"
        },
        {
            "endpoint": "GET /cn/cuotas/?residente_id={id}",  
            "prioridad": "🔴 ALTA",
            "razon": "Filtrar cuotas por residente específico"
        },
        {
            "endpoint": "GET /ad/residentes/mis-datos/{usuario_id}/",
            "prioridad": "🟡 MEDIA",
            "razon": "Perfil personalizado del residente"
        },
        {
            "endpoint": "GET /api/ai/eventos-acceso/",
            "prioridad": "🔴 ALTA", 
            "razon": "Log de accesos para guardias"
        },
        {
            "endpoint": "POST /api/ai/registrar-evento-manual/",
            "prioridad": "🟡 MEDIA",
            "razon": "Registro manual de visitas por guardias"
        },
        {
            "endpoint": "GET /api/ai/eventos-sospechosos/",
            "prioridad": "🟠 MEDIA-ALTA",
            "razon": "Alertas de seguridad para guardias"
        },
        {
            "endpoint": "GET /api/dashboard/residente/{id}/",
            "prioridad": "🟡 MEDIA",
            "razon": "Dashboard resumen para residentes"
        },
        {
            "endpoint": "GET /api/dashboard/guardia/",
            "prioridad": "🟡 MEDIA", 
            "razon": "Dashboard estadísticas para guardias"
        },
        {
            "endpoint": "POST /notificaciones/push/",
            "prioridad": "🟠 MEDIA-ALTA",
            "razon": "Sistema de notificaciones push"
        }
    ]
    
    return faltantes

def pantallas_sugeridas_app():
    """
    📱 PANTALLAS SUGERIDAS PARA LA APP MÓVIL
    """
    
    pantallas = {
        "COMUNES": [
            "🔐 Login/Splash",
            "👤 Perfil de usuario", 
            "⚙️ Configuraciones",
            "📱 Notificaciones"
        ],
        
        "PERFIL_RESIDENTE": [
            "🏠 Dashboard principal (cuotas pendientes, avisos)",
            "💰 Mis cuotas (pendientes/historial)",
            "💳 Realizar pago (seleccionar concepto + método)",
            "📸 Subir comprobante de pago",
            "📅 Reservas de áreas comunes",
            "➕ Nueva reserva",
            "📢 Avisos del condominio",
            "🚗 Mis vehículos registrados",
            "📊 Estadísticas de pagos"
        ],
        
        "PERFIL_GUARDIA": [
            "🎯 Dashboard monitoreo (eventos del día)",
            "📸 Escáner facial (cámara + resultado)",
            "🚗 Escáner de placas (cámara + resultado)",
            "📋 Log de accesos (historial eventos)",
            "👥 Directorio residentes",
            "🚙 Directorio vehículos", 
            "✍️ Registro manual de visitas",
            "🚨 Alertas de seguridad",
            "📊 Estadísticas del turno",
            "📱 Enviar notificaciones urgentes"
        ]
    }
    
    return pantallas

# FUNCIÓN PRINCIPAL
def main():
    print("="*80)
    print("📱 ENDPOINTS PARA APP MÓVIL - CONDOMINIUM")
    print("="*80)
    print("🎯 Enfoque: RESIDENTES + GUARDIAS (Pagos + Monitoreo)")
    print()
    
    endpoints = endpoints_para_app_movil()
    
    for categoria, eps in endpoints.items():
        print(f"\n🔹 {categoria}")
        print("-" * 50)
        
        for endpoint, info in eps.items():
            print(f"\n📍 {endpoint}")
            print(f"   📝 {info['descripcion']}")
            
            if 'body' in info:
                print(f"   📤 Body: {info['body']}")
            
            if 'query_params' in info:
                params = ', '.join([f"{k}={v}" for k, v in info['query_params'].items()])
                print(f"   🔍 Params: {params}")
            
            if 'uso_app' in info:
                print(f"   📱 Uso: {info['uso_app']}")
    
    print("\n" + "="*80)
    print("⚠️ ENDPOINTS FALTANTES POR CREAR")
    print("="*80)
    
    faltantes = endpoints_faltantes_por_crear()
    for item in faltantes:
        print(f"{item['prioridad']} {item['endpoint']}")
        print(f"     💡 {item['razon']}")
        print()
    
    print("="*80)
    print("📱 PANTALLAS SUGERIDAS PARA LA APP")
    print("="*80)
    
    pantallas = pantallas_sugeridas_app()
    for perfil, screens in pantallas.items():
        print(f"\n{perfil}:")
        for screen in screens:
            print(f"   {screen}")
    
    print("\n" + "="*80)
    print("🚀 RESUMEN PARA DESARROLLO")
    print("="*80)
    print("✅ Endpoints existentes: ~15 listos para usar")
    print("⚠️ Endpoints a crear: 9 adicionales necesarios")
    print("📱 Pantallas estimadas: 20-25 screens")
    print("⏱️ Tiempo estimado backend: 2-3 semanas")
    print("📱 Tiempo estimado app móvil: 4-6 semanas")
    print("💡 Stack recomendado: React Native + Expo")

if __name__ == "__main__":
    main()