class TableWaitingTime {
    constructor(importedData = null) {
        this.tableBody = $('#waitingTimeTableBody');
        this.numberOfApplications = parseInt($("input[name='applications']").val()) || 3;
        this.development_id = $('#selected-element-id').val();
        this.waitingTimesData = [];  

        if (importedData) {
            this.loadFromImport(importedData);
        } else {
            this.generateEmptyRows();
        }
    }

    generateEmptyRows() {
        const numberOfApps = parseInt($("input[name='applications']").val()) || 3;
        

        if (!this.tableBody.length) {
            return;
        }

        this.eliminateRows();
        
        for (let i = 1; i <= numberOfApps; i++) {
            const existingData = this.waitingTimesData.find(item => parseInt(item.application) === i);
            const waitTime = existingData ? existingData.waitTime : 3;
            this.appendRow(i, waitTime);

        }

    }

    eliminateRows() {
        this.tableBody.empty();
    }

    appendRow(id, value) {
        const row = `
            <tr class="row_waiting_time" id="row_waiting_time_${id}">
                <td>${id}</td>
                <td>
                    <input type="number" class="form-control" name="waiting_time_${id}" value="${value}">
                </td>
            </tr>
        `;
        this.tableBody.append(row);
    }

    loadFromImport(importedData) {
        this.waitingTimesData = importedData || [];
        this.generateEmptyRows();
    }

    updateWaitingTimesData() {
        this.waitingTimesData = this.getValues();
    }

    getValues() {
        let waitingTimes = [];
        $('.row_waiting_time input').each(function () {
            let appId = $(this).attr('name').split('_')[2];
            let waitTime = $(this).val();
            waitingTimes.push({ application: appId, waitTime: waitTime });
        });
        return waitingTimes;
    }
}
