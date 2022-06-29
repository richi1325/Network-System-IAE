const edit_row = (index) => {
    location.href='/#top'
    const row = document.getElementById(index);
    const data = {}
    data["ip"] = row.children[0].innerText
    data["mac"] = row.children[1].innerText
    data["descripcion"] = row.children[2].innerText
    data["propietario"] = propietarios_js[row.children[4].innerText]
    data["modelo"] = modelos_js[row.children[5].innerText]

    const prop = row.children[4].innerText
    const mode = row.children[5].innerText

    data["extension"] = row.children[6].innerText
    
    const div = document.getElementById("editar");
    const var_last = JSON.stringify(data)
    div.innerHTML = `
    <div class="shadow-md rounded px-8 pt-2 pb-8 mb-2 bg-white">
        <form action="/update" method="POST">
            <h1 class="titulo_form">
                Edita la IP:
            </h1>
            <div class="flex flex-col justify-around">
                <div class="flex flex-row justify-around">
                    <div class="flex flex-col ">
                        <div class="mb-2">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
                                IP:
                            </label>
                            <input
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                id="ip" type="text" name="ip" placeholder=""  value="${data["ip"]}" required readonly>
                        </div>
                        <div class="mb-2">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="mac">
                                Dirección MAC:
                            </label>
                            <input
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                id="mac" type="text" name="mac" placeholder="" value="${data["mac"]}">
                        </div>
                        <div class="mb-2">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="extension">
                                Extensión:
                            </label>
                            <input
                                class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                id="extension" type="text" name="extension" placeholder="" value="${data["extension"]}">
                        </div>
                    </div>
                    <div class="flex flex-col pb-2">
                        <label class="block text-gray-700 text-sm font-bold mb-2" for="descripcion">
                            Descripción:
                        </label>
                        <textarea
                            class="h-full shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            rows="8" cols="23" id="descripcion" name="descripcion">${data["descripcion"]}</textarea>
                    </div>
                </div>
            </div>
            <div class="flex flex-row justify-around">
                <div class="flex flex-col">
                    <div class="mb-2">
                        <label class="block text-gray-700 text-sm font-bold mb-2" for="propietario_id">
                            Propietario:
                        </label>
                        <select
                            class="block text-gray-700 border rounded w-full py-3 px-4 pr-8 text-gray-700 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                            id="propietario_id" name="propietario_id" required>
                        </select>
                    </div>
                    <div class="mb-2" id="otro_propietario">
                    </div>
                </div>
                <div class="mb-2">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="modelo_id">
                        Modelo:
                    </label>
                    <select
                        class="block text-gray-700 border rounded w-full py-3 px-4 pr-8 text-gray-700 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                        id="modelo_id" name="modelo_id" required>
                    </select>
                    <div class="mb-2" id="otro_modelo">
                    </div>
                </div>
                <div class="hidden">
                    <textarea id="last" name="last">${var_last}</textarea>
                </div>
            </div>
            <div>
                <div class="flex flex-row justify-center">
                    <input 
                        class="bg-blue-900 hover:bg-blue-400 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="button"
                        onclick="location.href='/'"
                        value="Cancelar">
                    </input>
                    <input
                        class="bg-blue-900 hover:bg-blue-400 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="submit" value="Actualizar">
                    </input>
                </div>
            </div>
        </form>
    </div>`;

    const prop_id = document.getElementById("propietario_id");
    html = ""
    for(element in propietarios_js){
        if(element == prop){
            html += `<option selected value='${propietarios_js[element]}'>${element}</option>` 
        } else {
            html += `<option value='${propietarios_js[element]}'>${element}</option>`
        }
    }
    html += `<option value="Otro:">Otro:</option>`;
    prop_id.innerHTML = html

    prop_id.addEventListener("change", function () {
        const propietario_div = document.getElementById("otro_propietario");
        if (this.value === "Otro:") {
            propietario_div.outerHTML = `
                <div class="mb-2" id="otro_propietario">                        
                <p class="text-gray-700 text-sm font-bold w-full py-2">
                    Nombre del propietario:
                </p>
                <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="propietario-input" type="text" name="propietario-input" placeholder="" required>
                </div>`;
        } else {
            propietario_div.outerHTML = `
                <div class="mb-2" id="otro_propietario">
                </div>`;
        }
    });

    const model_id = document.getElementById("modelo_id");
    html = ""
    for(element in modelos_js){
        if(element == mode){
            html += `<option selected value='${modelos_js[element]}'>${element}</option>` 
        } else {
            html += `<option value='${modelos_js[element]}'>${element}</option>`
        }
    }
    html += `<option value="Otro:">Otro:</option>`;
    model_id.innerHTML = html

    model_id.addEventListener("change", function () {
        const modelo_div = document.getElementById("otro_modelo");
        if (this.value === "Otro:") {
            modelo_div.outerHTML = `
                <div class="mb-2" id="otro_modelo">                        
                <p class="text-gray-700 text-sm font-bold w-full py-2">
                    Nombre del modelo:
                </p>
                <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="modelo-input" type="text" name="modelo-input" placeholder="" required>
                </div>`;
        } else {
            modelo_div.outerHTML = `
                <div class="mb-2" id="otro_modelo">
                </div>`;
        }
    });
}
