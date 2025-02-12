package com.example.rent.web;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

@RestController
public class RentalService {

    Logger logger = LoggerFactory.getLogger(RentalService.class);

    @GetMapping("/bonjour")
    public String disBonjour(){
        return "Bonjour";
    }

    @PutMapping(value = "/cars/{plateNumber}")
    public void rent(
            @PathVariable("plateNumber") String plateNumber,
            @RequestParam(value="rent") boolean rent,
            @RequestBody Dates dates){

        logger.info("PlateNumber : " + plateNumber);
        logger.info("Rent : " + rent);
        logger.info("Dates : " + dates);


    }

}
