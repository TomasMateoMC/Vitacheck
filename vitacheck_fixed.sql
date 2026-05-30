-- ============================================================
-- VITACHECK — Base de datos corregida
-- Cambios clave:
--   · Roles limpios: 1=admin, 2=medico
--   · medicos.usuario_id → une tabla medicos con usuarios
--   · historias_clinicas.medico_id → medicos.id (consistente)
--   · Datos limpios y coherentes
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


-- ------------------------------------------------------------
-- 1. ROLES
-- ------------------------------------------------------------
CREATE TABLE roles (
  id      INT         NOT NULL AUTO_INCREMENT,
  nombre  VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_rol (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO roles VALUES
  (1, 'admin'),
  (2, 'medico');

-- ------------------------------------------------------------
-- 2. USUARIOS  (cuentas de login)
-- ------------------------------------------------------------
CREATE TABLE usuarios (
  id              INT          NOT NULL AUTO_INCREMENT,
  username        VARCHAR(100) NOT NULL,
  password_hash   VARCHAR(255) NOT NULL,
  nombre_completo VARCHAR(150) DEFAULT NULL,
  role_id         INT          NOT NULL,
  created_at      TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_username (username),
  KEY fk_usr_rol (role_id),
  CONSTRAINT fk_usr_rol FOREIGN KEY (role_id) REFERENCES roles (id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Contraseñas: admin=admin123 | médicos=medico123
-- (hashes generados con werkzeug scrypt)
INSERT INTO usuarios (id, username, password_hash, nombre_completo, role_id) VALUES
  (1, 'admin',      'scrypt:32768:8:1$K7P25Goddxru7aP0$708733622387cc37d1baf39449979779e9d2be4b20891529143519562b60e3f60ccd52ecc29cf09acb9065a011b7d59800536a52ee508a64c44ac476d2dab0dc', 'Administrador del Sistema', 1),
  (2, 'dra.laura',  'scrypt:32768:8:1$7jIE77Y0PT4nQA4h$a085153053203ee090770d343a21a7e6ecb8464a5ef179cc28614fe1b7877aab86180cc35ac5a1641a0378799a484d830a2a22251ad912bd786b8c0c6cf89f4c', 'Dra. Laura Pérez',   2),
  (3, 'dr.carlos',  'scrypt:32768:8:1$7jIE77Y0PT4nQA4h$a085153053203ee090770d343a21a7e6ecb8464a5ef179cc28614fe1b7877aab86180cc35ac5a1641a0378799a484d830a2a22251ad912bd786b8c0c6cf89f4c', 'Dr. Carlos Gómez',   2),
  (4, 'dr.jhonatan','scrypt:32768:8:1$7jIE77Y0PT4nQA4h$a085153053203ee090770d343a21a7e6ecb8464a5ef179cc28614fe1b7877aab86180cc35ac5a1641a0378799a484d830a2a22251ad912bd786b8c0c6cf89f4c', 'Dr. Jhonatan Acevedo', 2);

-- ------------------------------------------------------------
-- 3. ESPECIALIDADES
-- ------------------------------------------------------------
CREATE TABLE especialidades (
  id          INT          NOT NULL AUTO_INCREMENT,
  nombre      VARCHAR(120) NOT NULL,
  descripcion TEXT         DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_esp (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO especialidades VALUES
  (1, 'Medicina General', 'Atención primaria y consulta general'),
  (2, 'Cardiología',      'Especialidad cardiovascular'),
  (3, 'Pediatría',        'Atención médica a niños y adolescentes');

-- ------------------------------------------------------------
-- 4. MEDICOS  (datos clínicos + enlace a su cuenta de usuario)
-- ------------------------------------------------------------
CREATE TABLE medicos (
  id               INT          NOT NULL AUTO_INCREMENT,
  usuario_id       INT          NOT NULL,   -- ← ENLACE con usuarios
  nombre           VARCHAR(150) NOT NULL,
  numero_licencia  VARCHAR(80)  DEFAULT NULL,
  specialty_id     INT          NOT NULL,
  telefono         VARCHAR(30)  DEFAULT NULL,
  email            VARCHAR(150) DEFAULT NULL,
  created_at       TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_licencia    (numero_licencia),
  UNIQUE KEY uq_usuario     (usuario_id),      -- 1 médico = 1 cuenta
  KEY fk_med_esp (specialty_id),
  CONSTRAINT fk_med_usr FOREIGN KEY (usuario_id)   REFERENCES usuarios      (id) ON DELETE CASCADE,
  CONSTRAINT fk_med_esp FOREIGN KEY (specialty_id) REFERENCES especialidades (id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO medicos (id, usuario_id, nombre, numero_licencia, specialty_id, telefono, email) VALUES
  (1, 2, 'Dra. Laura Pérez',    'LIC-1001', 1, '+57 3001112222', 'laura.perez@vitacheck.com'),
  (2, 3, 'Dr. Carlos Gómez',    'LIC-1002', 2, '+57 3003334444', 'carlos.gomez@vitacheck.com'),
  (3, 4, 'Dr. Jhonatan Acevedo','LIC-1003', 1, '+57 3212521232', 'jhonatan.acevedo@vitacheck.com');

-- ------------------------------------------------------------
-- 5. PACIENTES
-- ------------------------------------------------------------
CREATE TABLE pacientes (
  id               INT          NOT NULL AUTO_INCREMENT,
  nombre           VARCHAR(150) NOT NULL,
  documento        VARCHAR(50)  DEFAULT NULL,
  fecha_nacimiento DATE         DEFAULT NULL,
  genero           VARCHAR(20)  NOT NULL DEFAULT '',
  grupo_sanguineo  VARCHAR(5)   NOT NULL DEFAULT '',
  telefono         VARCHAR(30)  DEFAULT NULL,
  email            VARCHAR(150) DEFAULT NULL,
  direccion        VARCHAR(250) DEFAULT NULL,
  alergias         VARCHAR(255) DEFAULT NULL,
  created_at       TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_documento (documento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO pacientes (id, nombre, documento, fecha_nacimiento, genero, grupo_sanguineo, telefono, email, direccion, alergias) VALUES
  (1,  'Juan Torres',          'CC123456',   '1985-04-10', 'Masculino',  'O+', '+57 3121112211', 'juan.torres@example.com',   'Calle 1 #2-3, Cúcuta',         NULL),
  (2,  'María López',          'CC987654',   '1992-11-01', 'Femenino',   'A+', '+57 3122223333', 'maria.lopez@example.com',   'Calle 4 #5-6, Cúcuta',         'Penicilina'),
  (3,  'Sebastián Anteliz',    '10913812',   '2005-02-08', 'Masculino',  'B+', '+57 3187935793', 'sebastian.anteliz@gmail.com','Barrio El Norte, Cúcuta',      NULL),
  (4,  'Heydi Ramírez',        '123456789',  '2000-02-23', 'Femenino',   'A-', '+57 3123456789', 'heydi.ramirez@gmail.com',   'Barrio La Libertad, Cúcuta',   NULL),
  (5,  'Luisa Fabiola Jaimes', '1090381227', '1987-06-01', 'Femenino',   'O-', '+57 3184826517', 'luisa.jaimes@gmail.com',    'Antigua vía Boconó, Urb El Cuji', NULL),
  (6,  'Pablo Ruiz',           '129235349',  '1978-06-12', 'Masculino',  'AB+','+57 3184826517', 'pablo.ruiz@gmail.com',      'Av. 0 #12-45, Cúcuta',         NULL),
  (7,  'José Delgado',         '123132654',  '2001-06-15', 'Masculino',  'B-', '+57 3184258654', 'jose.delgado@gmail.com',    'Barrio Blanco, Cúcuta',        NULL),
  (8,  'Edinson Caravello',    '19872345',   '1990-06-10', 'Masculino',  'A-', '+57 3156444837', 'edinson.caravello@gmail.com','Barrio Suroriental, Cúcuta',   'Cerveza'),
  (9,  'Jhonatan Acevedo',     '1004515626', '2001-02-02', 'Masculino',  'O+', '+57 3243243242', 'jhonatan.acevedo@gmail.com', 'Calle 10 #3-24, Cúcuta',      NULL);

-- ------------------------------------------------------------
-- 6. CATEGORIAS IMC
-- ------------------------------------------------------------
CREATE TABLE categorias (
  idCategoria   INT          NOT NULL AUTO_INCREMENT,
  nombre        VARCHAR(50)  NOT NULL,
  rangoMin      FLOAT        NOT NULL,
  rangoMax      FLOAT        NOT NULL,
  recomendacion TEXT         NOT NULL,
  PRIMARY KEY (idCategoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO categorias VALUES
  (1, 'Bajo peso',    0,     18.49, 'Bajo peso. Se sugiere aumentar el consumo calórico con nutrientes saludables.'),
  (2, 'Normal',       18.5,  24.99, 'Peso normal. Mantener una dieta equilibrada y actividad física constante.'),
  (3, 'Sobrepeso',    25,    29.99, 'Sobrepeso. Reducir azúcares y grasas, acompañado de ejercicio regular.'),
  (4, 'Obesidad I',   30,    34.99, 'Obesidad Grado I. Se recomienda plan cardiovascular y control nutricional.'),
  (5, 'Obesidad II',  35,    39.99, 'Obesidad Grado II. Consultar especialista médico para ajustar hábitos.'),
  (6, 'Obesidad III', 40,    999,   'Obesidad Grado III (Mórbida). Requiere intervención médica inmediata.');

-- ------------------------------------------------------------
-- 7. IMC HISTORIAL  (clasificación estandarizada)
-- ------------------------------------------------------------
CREATE TABLE imc_historial (
  id            INT            NOT NULL AUTO_INCREMENT,
  paciente_id   INT            NOT NULL,
  peso          DECIMAL(5,2)   NOT NULL,
  altura        DECIMAL(4,2)   NOT NULL,
  imc           DECIMAL(5,2)   NOT NULL,
  clasificacion VARCHAR(20)    NOT NULL,
  fecha         TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY fk_imc_pac (paciente_id),
  CONSTRAINT fk_imc_pac FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO imc_historial (paciente_id, peso, altura, imc, clasificacion, fecha) VALUES
  (1, 80.00, 1.89, 22.40, 'Normal',     '2025-11-23 15:38:47'),
  (1, 70.00, 1.80, 21.60, 'Normal',     '2025-11-23 17:46:15'),
  (2, 67.00, 1.69, 23.46, 'Normal',     '2025-11-23 16:05:49'),
  (2, 70.00, 1.73, 23.39, 'Normal',     '2025-11-23 16:18:12'),
  (3, 78.00, 1.80, 24.07, 'Normal',     '2025-11-23 15:26:04'),
  (4, 62.00, 1.70, 21.45, 'Normal',     '2025-11-23 14:51:42'),
  (4, 64.00, 1.70, 22.15, 'Normal',     '2025-11-23 15:02:24'),
  (5, 72.00, 1.67, 25.82, 'Sobrepeso',  '2025-11-23 15:05:20'),
  (6, 75.00, 1.82, 22.64, 'Normal',     '2025-11-23 18:12:34'),
  (7, 35.00, 1.35, 19.20, 'Normal',     '2025-11-23 18:51:36'),
  (8, 80.00, 1.67, 28.69, 'Sobrepeso',  '2025-11-23 18:55:23'),
  (8, 90.00, 1.65, 33.06, 'Obesidad I', '2026-05-28 03:40:30');

-- ------------------------------------------------------------
-- 8. HISTORIAS CLINICAS  (medico_id → medicos.id, consistente)
-- ------------------------------------------------------------
CREATE TABLE historias_clinicas (
  id          INT       NOT NULL AUTO_INCREMENT,
  paciente_id INT       NOT NULL,
  medico_id   INT       DEFAULT NULL,   -- ← ahora apunta a medicos.id
  fecha       DATETIME  DEFAULT CURRENT_TIMESTAMP,
  tipo        VARCHAR(80) DEFAULT NULL,
  nota        TEXT      NOT NULL,
  created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY fk_hc_pac (paciente_id),
  KEY fk_hc_med (medico_id),
  CONSTRAINT fk_hc_pac FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
  CONSTRAINT fk_hc_med FOREIGN KEY (medico_id)   REFERENCES medicos   (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO historias_clinicas (paciente_id, medico_id, tipo, nota) VALUES
  (1, 2, 'Consulta general', 'Paciente presenta fuertes dolores de cabeza y vómito constante. Se solicita examen neurológico.'),
  (8, 1, 'Control de peso',  'Paciente con tendencia al sobrepeso. Se inicia plan nutricional y rutina de ejercicio semanal.');

-- ------------------------------------------------------------
-- 9. CITAS MEDICAS
-- ------------------------------------------------------------
CREATE TABLE citas (
  id          INT          NOT NULL AUTO_INCREMENT,
  paciente_id INT          NOT NULL,
  medico_id   INT          NOT NULL,
  fecha       DATE         NOT NULL,
  hora        TIME         NOT NULL,
  estado      ENUM('pendiente','programada','completada','cancelada')
              NOT NULL DEFAULT 'pendiente',
  motivo      VARCHAR(250) DEFAULT NULL,
  created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY fk_cita_pac (paciente_id),
  KEY fk_cita_med (medico_id),
  KEY idx_fecha   (fecha),
  KEY idx_estado  (estado),
  CONSTRAINT fk_cita_pac FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
  CONSTRAINT fk_cita_med FOREIGN KEY (medico_id)   REFERENCES medicos   (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO citas (paciente_id, medico_id, fecha, hora, estado, motivo) VALUES
  (1, 2, '2026-06-10', '15:14:00', 'pendiente',  'Dolor fuerte en pierna derecha'),
  (2, 1, '2026-05-12', '06:49:00', 'completada', 'Control general'),
  (3, 3, '2026-07-01', '09:00:00', 'programada', 'Primera consulta');

-- ------------------------------------------------------------
-- 10. MENSAJES (chat entre usuarios)
-- ------------------------------------------------------------
CREATE TABLE mensajes (
  id               INT       NOT NULL AUTO_INCREMENT,
  remitente_id     INT       NOT NULL,
  destinatario_id  INT       NOT NULL,
  contenido        TEXT      NOT NULL,
  leido            TINYINT   DEFAULT 0,
  fechaEnvio       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY fk_msg_rem  (remitente_id),
  KEY fk_msg_dest (destinatario_id),
  CONSTRAINT fk_msg_rem  FOREIGN KEY (remitente_id)    REFERENCES usuarios (id) ON DELETE CASCADE,
  CONSTRAINT fk_msg_dest FOREIGN KEY (destinatario_id) REFERENCES usuarios (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO mensajes (remitente_id, destinatario_id, contenido, leido) VALUES
  (1, 2, 'Hola Dra. Laura, tiene una cita programada para mañana.', 0),
  (2, 1, 'Gracias, ya estoy al tanto. ¿Confirmo la hora?',          1),
  (1, 3, 'Dr. Carlos, hay un paciente nuevo asignado a su agenda.',  0);

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- RESUMEN DE ACCESOS:
--   admin      / admin123   → Panel administración
--   dra.laura  / medico123  → Panel médico
--   dr.carlos  / medico123  → Panel médico
--   dr.jhonatan/ medico123  → Panel médico
-- ============================================================
