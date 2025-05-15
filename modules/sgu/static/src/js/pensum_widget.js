/** @odoo-module **/

import { Component, useState, useRef, onMounted, nextTick } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { sprintf } from "@web/core/utils/strings";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

export class PensumWidget extends Component {
  static template = "sgu.PensumWidgetTemplate";
  static tag = "sgu.PensumWidget";

  setup() {
    // Servicios
    this.rpc = rpc;                                  // función RPC
    this.actionService = useService("action");       // sirve para doAction
    this.notificationService = useService("notification");
    this.ormService = useService("orm");

    // Estado
    this.state = useState({
      modalidades: [],  // Ahora se cargarán desde el modelo
      niveles: [],
      carreras: [],
      modalidad: null,
      nivel_academico: null,
      carrera: null,
      codigo_principal: 0,
      periodCount: 1,
      selectedDivision: 1,
      rows: [],
      selectedTray: [],
      // Refs
      isTrimestreMode: false, // Nuevo campo para activar modo trimestre
      modalidadSelect: useRef("modalidadSelect"),
      nivelSelect: useRef("nivelSelect"),
      carreraSelect: useRef("carreraSelect"),
      codigoPrincipalInput: useRef("codigoPrincipalInput"),
      divisionSelect: useRef("divisionSelect"),
      inputCodigo: useRef("inputCodigo"),
      inputAsignatura: useRef("inputAsignatura"),
      inputUC: useRef("inputUC"),
      inputHT: useRef("inputHT"),
      inputHP: useRef("inputHP"),
      inputPrelacionAsignaturas: useRef("inputPrelacionAsignaturas"),
      inputPrelacionUC: useRef("inputPrelacionUC"),
      inputPrelacionGaceta: useRef("inputPrelacionGaceta"),
      trimestresDiv: useRef("trimestresDiv"),
      prelacionGacetaLabel: useRef("prelacionGacetaLabel"),
    });

    this.pensumId = null;

    onMounted(async () => {
      // Cargar modalidades
      this.state.modalidades = await this.ormService.searchRead(
          'sgu_modalidad',
          [['active', '=', true]],
          ['id', 'modalidad']
      );
      
      // Cargar niveles académicos
      this.state.niveles = await this.ormService.searchRead(
          'sgu_nivel_academico',
          [['active', '=', true]],
          ['id', 'nivel']
      );
      
      // Cargar carreras
      this.state.carreras = await this.ormService.searchRead(
          'sgu_carreras',
          [['active', '=', true]],
          ['id', 'carrera']
      );
      this._renderDivisions();
      this._toggleTrimestreElements();
      if (this.props.action.res_id) {
        this.pensumId = this.props.action.res_id;
        await this._loadPensum(this.pensumId);
      }
    });
    
  }
// En la clase PensumWidget (dentro del setup)

// En la clase PensumWidget (dentro del setup)
// En tu componente OWL (archivo JavaScript)
getDivisionLabel(textoModalidad, modoTrayectoActivo) {
  console.log('[getDivisionLabel] Iniciando. textoModalidad:', textoModalidad, ', modoTrayectoActivo:', modoTrayectoActivo);

  // NUEVA CONDICIÓN: Si el "Modo Trayecto" (checkbox) está activo,
  // la etiqueta siempre debe ser "Trayecto".
  if (modoTrayectoActivo) {
    console.log('[getDivisionLabel] "Modo Trayecto" (checkbox) está ACTIVO. Devolviendo "Trayecto".');
    return 'Trayecto';
  }

  // Si el "Modo Trayecto" (checkbox) NO está activo, se aplica la lógica anterior:
  console.log('[getDivisionLabel] "Modo Trayecto" (checkbox) está INACTIVO.');
  if (textoModalidad) {
    console.log('[getDivisionLabel] textoModalidad tiene un valor:', textoModalidad);
    return textoModalidad; // Devuelve el nombre de la modalidad (ej. "Semestre", "Trimestre")
  }

  console.log('[getDivisionLabel] textoModalidad está vacío o nulo. Devolviendo "Trayecto" (fallback).');
  return 'Trayecto'; // Fallback si no hay textoModalidad y el checkbox no está activo
}
  // --- División / pre­lación ---
  _updateDivisionOptions() {
    if (this.state.selectedDivision > this.state.periodCount) {
      this.state.selectedDivision = this.state.periodCount;
    }
  }

  _increasePeriods() {
    this.state.periodCount++;
    this._renderDivisions();
  }

  _decreasePeriods() {
    if (this.state.periodCount > 1) {
      this.state.periodCount--;
      this._renderDivisions();
    }
  }

  _renderDivisions() {
    this._updateDivisionOptions();
    this._renderPrelacionAsignaturasOptions();
    this._updatePrelacionUCMax();
  }

  _getRowsBefore(div) {
    return this.state.rows.filter(r => r.division < div);
  }

  _sumUCBefore(div) {
    return this._getRowsBefore(div).reduce((sum, r) => sum + (parseInt(r.uc)||0), 0);
  }

  _renderPrelacionAsignaturasOptions() {
    const sel = this.state.inputPrelacionAsignaturas.el;
    if (!sel) return;
    sel.innerHTML = "";
    const curDiv = parseInt(this.state.divisionSelect.el.value)||1;
    this._getRowsBefore(curDiv)
      .map(r=>r.asignatura)
      .filter((v,i,a)=>v && a.indexOf(v)===i)
      .forEach(text => {
        const opt = document.createElement("option");
        opt.value = text; opt.textContent = text;
        sel.appendChild(opt);
      });
  }

  _updatePrelacionUCMax() {
    const inp = this.state.inputPrelacionUC.el;
    if (!inp) return;
    const curDiv = parseInt(this.state.divisionSelect.el.value)||1;
    const max = this._sumUCBefore(curDiv);
    inp.max = max;
    if (+inp.value > max) inp.value = max;
  }

  _onDivisionChange() {
    this.state.selectedDivision = parseInt(this.state.divisionSelect.el.value)||1;
    this._renderPrelacionAsignaturasOptions();
    this._updatePrelacionUCMax();
  }

  // --- Asignaturas ---
  _addAssignment() {
    if (this.state.isTrimestreMode && this.state.selectedTray.length === 0) {
      this.notificationService.add('Seleccione al menos un trimestre.', {type: 'warning'});
      return;
  }
    const div = parseInt(this.state.divisionSelect.el.value)||1;
    const codigo = this.state.inputCodigo.el.value;
    const asig = this.state.inputAsignatura.el.value;
    const uc = parseInt(this.state.inputUC.el.value)||0;
    const ht = parseInt(this.state.inputHT.el.value)||0;
    const hp = parseInt(this.state.inputHP.el.value)||0;
    const prelAsigs = Array.from(this.state.inputPrelacionAsignaturas.el.selectedOptions)
                          .map(o => o.value);
    const prelUC = parseInt(this.state.inputPrelacionUC.el.value)||0;
    const prelG = this.state.inputPrelacionGaceta.el.value;
    const maxUC = this._sumUCBefore(div);

    if (prelUC<0 || prelUC>maxUC) {
      this.notificationService.add(sprintf('Prelación UC debe estar entre 0 y %s', maxUC), {type:'warning'});
      return;
    }
    if (this.state.modalidad==='trimestre' && this.state.selectedTray.length===0) {
      this.notificationService.add('Seleccione al menos un trimestre.', {type:'warning'});
      return;
    }
    if (!asig) {
      this.notificationService.add('Asignatura es requerida.', {type:'warning'});
      return;
    }
    if (uc<=0) {
      this.notificationService.add('UC debe ser mayor a 0.', {type:'warning'});
      return;
    }

    // Usar el array directamente, no convertirlo a string
    const trays = this.state.isTrimestreMode 
        ? [...this.state.selectedTray] 
        : [];

        this.state.rows.push({
          division: div,
          codigo: codigo ? parseInt(codigo) : null,
          asignatura: asig,
          uc, ht, hp,
          tot: ht + hp,
          prelAsigs: prelAsigs || [], // Asegurar array vacío si no hay selección
          prelUC: prelUC,
          prelGaceta: prelG,
          trayectos: this.state.isTrimestreMode ? [...this.state.selectedTray] : [],
      });


    // Reset inputs
    [
      'inputCodigo','inputAsignatura','inputUC','inputHT',
      'inputHP','inputPrelacionUC','inputPrelacionGaceta'
    ].forEach(id => this.state[id].el.value = '');
    this.state.inputPrelacionAsignaturas.el.selectedIndex = -1;
    this.state.selectedTray = [];

    this._renderPrelacionAsignaturasOptions();
    this._updatePrelacionUCMax();
  }

  _onTrayButtonClick(ev) {
    const tray = parseInt(ev.currentTarget.dataset.tray, 10);
    const idx = this.state.selectedTray.indexOf(tray);
    if (idx>=0) this.state.selectedTray.splice(idx,1);
    else this.state.selectedTray.push(tray);
    this.state.selectedTray.sort((a,b)=>a-b);
  }

  // --- Modalidad / UI tweaks ---
// Tu _onModalidadChange, mejorado para manejar la opción vacía
_onModalidadChange() {
  const selectElement = this.state.modalidadSelect.el; // O como accedas a tu <select>
                                                     // Si usas t-ref="modalidadSelect", y en setup(): this.modalidadSelectRef = useRef("modalidadSelect");
                                                     // entonces sería: const selectElement = this.modalidadSelectRef.el;

  const modalidadIdValue = selectElement.value; // Esto será un string "1", "2", o ""

  console.log('[_onModalidadChange] Valor seleccionado:', modalidadIdValue);

  if (!modalidadIdValue) { // Si es "" (opción "Seleccione una modalidad")
      this.state.modalidad = null; // Limpia la modalidad
      console.log('[_onModalidadChange] Ninguna modalidad seleccionada, this.state.modalidad es null.');
      return;
  }

  const modalidadId = parseInt(modalidadIdValue);
  this.state.modalidad = this.state.modalidades.find(m => m.id === modalidadId);
  console.log('[_onModalidadChange] this.state.modalidad actualizado a:', this.state.modalidad);
}


  _toggleTrimestreElements() {
    const trayDiv = this.state.trimestresDiv.el;
    const gacLabel = this.state.prelacionGacetaLabel.el;
    
    if (trayDiv) trayDiv.style.display = this.state.isTrimestreMode ? 'flex' : 'none';
    if (gacLabel) gacLabel.style.display = this.state.isTrimestreMode ? '' : 'none';
    this.state.selectedTray = [];
  }

  _onBasicConfigChange() {
    const nivelId = parseInt(this.state.nivelSelect.el.value);
    this.state.nivel_academico = this.state.niveles.find(n => n.id === nivelId);
    
    const carreraId = parseInt(this.state.carreraSelect.el.value);
    this.state.carrera = this.state.carreras.find(c => c.id === carreraId);
}

  // --- Guardar / cargar con ORMService ---
  async _onSavePensum() {
    // Validar IDs de relaciones Many2one
    if (!this.state.modalidad?.id || !this.state.nivel_academico?.id || !this.state.carrera?.id) {
        this.notificationService.add('Seleccione Modalidad, Nivel y Carrera.', {type:'warning'});
        return;
    }

    // Convertir trayectos a string
    const rowsToSave = this.state.rows.map(row => ({
        ...row,
        trayectos: row.trayectos.join(','),
    }));

    // Preparar datos
    const data = {
        modalidad: this.state.modalidad?.id,
        nivel_academico: this.state.nivel_academico?.id,
        carrera: this.state.carrera?.id,
        codigo_principal: parseInt(this.state.codigo_principal) || 0,
        period_count: this.state.periodCount,
        is_trimestre_mode: this.state.isTrimestreMode,
        assignment_data: JSON.stringify(rowsToSave),
    };

    console.log('Datos a guardar:', data); // Verificar en consola

    
    try {
      let res;
      if (this.pensumId) {
        this.pensumId = parseInt(this.pensumId, 10);
        res = await this.ormService.write('sgu.pensum', [this.pensumId], data);
      } else {
        res = await this.ormService.create('sgu.pensum', [data]);
        this.pensumId = res[0];  // <- ¡Corregido aquí!
      }
      if (this.pensumId) {
        this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'sgu.pensum',
          res_id: this.pensumId,
          views: [[false,'form']],
          target: 'current',
        });
      }
    } catch (e) {
      this.notificationService.add('Error al guardar.',{type:'danger'});
      console.error(e);
    }
  }

  async _onNewPensum() {
    this.pensumId = null;
    Object.assign(this.state, {
      modalidad: { id: null, name: 'Trimestre' }, // ✅ Objeto con estructura Many2one
      nivel_academico: null,
      carrera: null,
      codigo_principal: 0,
      periodCount: 1,
      selectedDivision:1,
      rows: [], selectedTray: [],
    });
    [
      'inputCodigo','inputAsignatura','inputUC','inputHT',
      'inputHP','inputPrelacionAsignaturas','inputPrelacionUC','inputPrelacionGaceta'
    ].forEach(id => {
      const el = this.state[id].el;
      if (el) el.value = id==='inputPrelacionAsignaturas'? null : '';
    });
    this._renderDivisions();
    this._toggleTrimestreElements();
    this.notificationService.add('Nuevo pensum iniciado.',{type:'info'});
  }

  async _loadPensum(id) {
    try {
        const [data] = await this.ormService.read('sgu.pensum', [id], [
            'modalidad', 'nivel_academico', 'carrera', 
            'codigo_principal', 'period_count', 'assignment_data'
        ]);
        // En el método _loadPensum (JS)
        rows.forEach(row => {
          if (typeof row.trayectos === 'string') {
              row.trayectos = row.trayectos.split(',').map(Number);
          }
        });
        if (data.assignment_data) {
          const rows = JSON.parse(data.assignment_data);
          
          // Convertir campos a arrays si son strings
          rows.forEach(row => {
              if (typeof row.prelAsigs === 'string') {
                  row.prelAsigs = row.prelAsigs.split(',');
              }
              if (typeof row.trayectos === 'string') {
                  row.trayectos = row.trayectos.split(',').map(Number);
              }
          });
          
          this.state.rows = rows;
      }
        
        if (!data) {
            this.notificationService.add('Pensum no encontrado.', {type: 'warning'});
            return;
        }

        // Obtener IDs y nombres de las relaciones
        this.state.modalidad = data.modalidad ? { id: data.modalidad[0], name: data.modalidad[1] } : null;
        this.state.nivel_academico = data.nivel_academico ? { id: data.nivel_academico[0], name: data.nivel_academico[1] } : null;
        this.state.carrera = data.carrera ? { id: data.carrera[0], name: data.carrera[1] } : null;
        this.state.isTrimestreMode = data.is_trimestre_mode || false;


        // Asignar otros campos
        this.state.codigo_principal = data.codigo_principal;
        this.state.periodCount = data.period_count;
        this.state.rows = data.assignment_data ? JSON.parse(data.assignment_data) : [];

        await nextTick();

        // Actualizar selects con los IDs
        if (this.state.modalidad) {
            this.state.modalidadSelect.el.value = this.state.modalidad.id;
        }
        if (this.state.nivel_academico) {
            this.state.nivelSelect.el.value = this.state.nivel_academico.id;
        }
        if (this.state.carrera) {
            this.state.carreraSelect.el.value = this.state.carrera.id;
        }

        this.state.codigoPrincipalInput.el.value = this.state.codigo_principal;
        this.state.divisionSelect.el.value = this.state.selectedDivision;
        this._renderDivisions();
        this._toggleTrimestreElements();
        this.notificationService.add('Pensum cargado.', {type: 'success'});
    } catch (e) {
        this.notificationService.add('Error cargando pensum.', {type: 'danger'});
        console.error(e);
    }
  }
}

// Registrar el widget
registry.category("actions").add("sgu.PensumWidget", PensumWidget);