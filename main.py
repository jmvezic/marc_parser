def parse_marc(files):
    records_to_return = []
    field_end = "\x1e"
    subfield = "\x1f"
    record_end = "\x1d"

    def split_to_each_field(n, value):
        lines = [value[i:i + n] for i in range(0, len(value), n)]
        return lines

    for file in files:
        with open(file, newline="", encoding="utf8", errors="replace") as marc_file:
            marc_file = marc_file.read()
            marc_records = marc_file.split(record_end)
            del marc_records[-1]
            for one_record in marc_records:
                temp_record = {}
                base_address = int(one_record[12:17])
                full_index = one_record[24:base_address - 1]
                fields_index = split_to_each_field(12, full_index)
                record_itself = one_record[base_address:]

                for field_info in fields_index:
                    tag = field_info[:3]
                    field_length = int(field_info[3:7])
                    starting_char_pos = int(field_info[7:12])
                    field_subfields = record_itself[starting_char_pos:starting_char_pos+field_length].split(subfield)
                    for fieldSubfield in field_subfields:
                        if fieldSubfield:
                            subfield_mark = fieldSubfield[0]
                            ready_subfield = fieldSubfield[1:].replace(field_end, "").replace(record_end, "")
                            if ready_subfield.strip():
                                if tag+subfield_mark in temp_record.keys():
                                    if type(temp_record[tag + subfield_mark]) is not list:
                                        temp_record[tag + subfield_mark] = [temp_record[tag+subfield_mark]]
                                        temp_record[tag+subfield_mark].append(ready_subfield)
                                    else:
                                        temp_record[tag + subfield_mark].append(ready_subfield)
                                else:
                                    temp_record[tag+subfield_mark] = ready_subfield

                records_to_return.append(temp_record)

    return records_to_return