class Table {
  constructor(headings, rows) {
    this.headings = headings;
    this.rows = rows;
    this.turn_num = 0;

    this.createTable();
    this.add_row = function(info_json) {
      this.turn += 1;
      info_json["n"] = this.turn_num;
      this.rows = [info_json];
      this.createRows();
    };
    
  }
  //CREATE TABLE
  createTable() {
    //MAKING A DIV
    const tableDiv = document.createElement("div");
    tableDiv.classList.add("side");
    tableDiv.id = "left-hand"
    const body = document.getElementById("place-of-table");
    body.appendChild(tableDiv);

    //MAKING A TABLE
    let table = document.createElement("table");
    table.classList.add("table")
    table.id ="info-table";
    tableDiv.appendChild(table);

    this.createHeadings();
  }

  //CREATE HEADINGS
  createHeadings() {
    let thead = document.createElement("thead"),
      trHeading = document.createElement("tr");

    this.headings.forEach(heading => {
      const th = document.createElement("th"),
        thContent = document.createTextNode(heading.label);

      th.appendChild(thContent);
      trHeading.appendChild(th);
    });

    let table = document.querySelector(".table");
    table.appendChild(thead);
    thead.appendChild(trHeading);

    this.createRows();
  }

  //CREATE ROWS
  createRows() {
    let tbody = document.createElement("tbody"),
      table = document.querySelector(".table");
    table.appendChild(tbody);

    this.rows.forEach(row => {
      let trRow = document.createElement("tr");
      trRow.classList.add("click-and-input");
      tbody.appendChild(trRow);

      const rowEntries = Object.entries(row);

      for (const [key, value] of rowEntries) {
        let headingsObj = this.headings.find(o => o.for == key);

        if (headingsObj) {
          let td = document.createElement("td");

          let tdContent = document.createTextNode(value);
          td.appendChild(tdContent);
          trRow.appendChild(td);
        } else if (!headingdObj) {
          let td = document.createElement("td");

          let tdContent = document.createTextNode("-");
          td.appendChild(tdContent);
          trRow.appendChild(td);
        }
      }
    });
  }
}

