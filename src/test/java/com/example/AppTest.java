package com.example;

import static org.junit.Assert.assertEquals;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;

import org.junit.Test;

public class AppTest {
//
  @Test
  public void listsFiles_flaky() throws IOException {
    Path dir = Files.createTempDirectory("d-");
    Files.createFile(dir.resolve("a.txt"));
    Files.createFile(dir.resolve("b.txt"));
    Files.createFile(dir.resolve("c.txt"));

    // This is the flaky part: File.list() does not guarantee order.
    List<String> names = Arrays.asList(dir.toFile().list());

    assertEquals(Arrays.asList("a.txt", "b.txt", "c.txt"), names);
  }

  @Test
  public void listsFiles_flaky2() throws IOException {
    Path dir = Files.createTempDirectory("d-");
    Files.createFile(dir.resolve("d.txt"));
    Files.createFile(dir.resolve("e.txt"));
    Files.createFile(dir.resolve("f.txt"));

    // This is the flaky part: File.list() does not guarantee order.
    List<String> names = Arrays.asList(dir.toFile().list());

    assertEquals(Arrays.asList("d.txt", "e.txt", "f.txt"), names);
  }
}